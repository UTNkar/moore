from datetime import date
from django.apps import apps
from django.contrib.auth.models import AbstractUser, UserManager
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin
from utils.utn_client import UTNClient
from utils.melos_client import MelosClient


class SSNValidator(validators.RegexValidator):
    def __init__(self):
        super(SSNValidator, self).__init__(
            # The regex checks for the formats: YYYYMMDD-XXXX, YYMMDD-XXXX
            # - Makes sure that the year is either 1900 or 2000
            regex=r'^[1-2][0|9][0-9]{2}[0-1][0-9][0-3][0-9][-][0-9]{4}$|^[0|9][0-9]{1}[0-1][0-9][0-3][0-9][-][0-9]{4}$',  # noqa: E501
            message=_(
                'Use the format YYYYMMDD-XXXX or YYMMDD-XXXX for your ssn.'
            )
        )


class CaseInsensitiveUsernameUserManager(UserManager):
    # Search username with insensitive case
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact' \
            .format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class MelosUserManager(CaseInsensitiveUsernameUserManager):
    # Search Member through Melos if username is SSN
    def get_by_natural_key(self, username):
        member = None
        try:
            member = super().get_by_natural_key(username)
        except Exception as e:
            member = Member.find_by_ssn(username)

            if member is None:
                raise e

        return member


class Member(SimpleEmailConfirmationUserMixin, AbstractUser):
    """This class describes a member"""

    # ---- AbstractUser overrides ---

    objects = MelosUserManager()

    # ---- Personal information ------

    birthday = models.DateField(
        verbose_name=_('Birthday'),
        null=True
    )

    person_number_ext = models.CharField(
        max_length=4,
        verbose_name=_('Person number extension'),
        help_text=_('Enter the last four digits of your Swedish person '
                    'number, given by the Swedish tax authority'),
        validators=[validators.RegexValidator(
            regex=r'^\d{4}$',
            message=_('The person number extension consists of four numbers'),
        )],
        unique_for_date="birthday",
        blank=True,
    )

    # ---- Membership information ------

    MEMBERSHIP_CHOICES = (
        ('unknown', _('Unknown')),
        ('nonmember', _('Nonmember')),
        ('member', _('Member')),
        ('alumnus', _('Alumnus')),
    )

    status = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_CHOICES,
        verbose_name=_('Membership status'),
        blank=False,
        default='unknown'
    )
    status_changed = models.DateTimeField(
        default=timezone.now,
        null=False,
    )

    # ---- Contact information ------

    phone_number = models.CharField(
        max_length=20,
        verbose_name=_('Phone number'),
        help_text=_('Enter a phone number so UTN may reach you'),
        blank=True,
    )

    # ---- University information ------

    registration_year = models.CharField(
        max_length=4,
        verbose_name=_('Registration year'),
        help_text=_('Enter the year you started studying at the TakNat '
                    'faculty'),
        validators=[validators.RegexValidator(
            regex=r'^\d{4}$',
            message=_('Please enter a valid year')
        )],
        blank=True,
    )

    study = models.ForeignKey(
        'StudyProgram',
        verbose_name=_('Study program'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    section = models.ForeignKey(
        'Section',
        verbose_name=_('Member of section'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # ---- Melos ------

    melos_id = models.IntegerField(
        blank=True,
        editable=False,
        null=True
    )

    def __str__(self) -> str:
        return self.username

    @property
    def teams(self):
        Team = apps.get_model('involvement', 'Team')
        return Team.objects.filter(
            roles__positions__term_from__lte=date.today(),
            roles__positions__term_to__gte=date.today(),
            roles__positions__applications__applicant=self,
            roles__positions__applications__status='appointed',
        )

    @property
    def roles(self):
        Role = apps.get_model('involvement', 'Role')
        return Role.objects.filter(
            positions__term_from__lte=date.today(),
            positions__term_to__gte=date.today(),
            positions__applications__applicant=self,
            positions__applications__status='appointed',
        )

    def person_number(self) -> str:
        if self.birthday is None or self.person_number_ext is None:
            return ''
        else:
            return '%s-%s' % (self.birthday.strftime('%Y%m%d'),
                              self.person_number_ext)

    def update_status(self, data=None):
        if data is None:
            if self.person_number() == '':
                return
            try:
                data = UTNClient.registration_status(
                    self.person_number().replace('-', ''))
            except ValueError:
                return

        if data == 'member':
            self.status = 'member'
        elif data == 'nonmember':
            if self.status in ['unknown', 'nonmember']:
                self.status = 'nonmember'
            else:
                self.status = 'alumnus'

        self.status_changed = timezone.now()

    def remove_old_email(self):
        for email in self.get_unconfirmed_emails() or []:
            self.remove_email(email)
        for email in self.get_confirmed_emails():
            if email != self.email:
                self.remove_email(email)

    def get_status_text(self, status):
        status = _('Member') if status == 'member' else _('Nonmember')
        return status

    @staticmethod
    def find_by_ssn(ssn):
        try:
            SSNValidator()(ssn)

            melos_id = MelosClient.get_melos_id(ssn)
            if melos_id is not False:
                return Member.objects.filter(melos_id=int(melos_id)).first()
        except Exception:
            pass

        return None
