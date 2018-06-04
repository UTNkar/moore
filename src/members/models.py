import requests
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.core import validators
from django.db import models
from django.db.models import ManyToManyField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from requests.auth import HTTPDigestAuth
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

from utils.translation import TranslatedField


class CaseInsensitiveUsernameUserManager(UserManager):
    # Get username by insensitive case
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

class Member(SimpleEmailConfirmationUserMixin, AbstractUser):
    """This class describes a member"""

    objects = CaseInsensitiveUsernameUserManager()

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
        validators=[validators.RegexValidator(
            regex=r'^\+?\d+$',
            message=_('Please enter a valid phone number'),
        )],
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

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return self.get_full_name()
        else:
            return self.username

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
                r = requests.get(
                    'https://register.utn.se/api.php',
                    auth=HTTPDigestAuth(settings.MEMBERSHIP_API_USER,
                                        settings.MEMBERSHIP_API_PASSWORD),
                    params={
                        'action': 'check',
                        'person_number': self.person_number().replace('-', '')
                    },
                )
                data = r.json().get('status')
            except requests.exceptions.ConnectionError:
                data = 'unknown'
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


class Section(models.Model):
    """This class represent a study section"""

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')

    name_en = models.CharField(
        max_length=255,
        verbose_name=_('English section name'),
        help_text=_('Enter the name of the section'),
        blank=False,
    )

    name_sv = models.CharField(
        max_length=255,
        verbose_name=_('Swedish section name'),
        help_text=_('Enter the name of the section'),
        blank=False,
    )

    name = TranslatedField('name_en', 'name_sv')

    abbreviation = models.CharField(
        max_length=130,
        verbose_name=_('Section abbreviation'),
        help_text=_('Enter the abbreviation for the section'),
        blank=True,
    )

    studies = ManyToManyField(
        'StudyProgram',
        related_name='sections',
        blank=True,
    )

    def __str__(self) -> str:
        if self.abbreviation:
            return '%s - %s' % (self.abbreviation, self.name)
        else:
            return self.name.__str__()


class StudyProgram(models.Model):
    """This class describes a university study program"""

    class Meta:
        verbose_name = _('study program')
        verbose_name_plural = _('study programs')

    DEGREE_CHOICES = (
        ('bsc', _('Bachelor of Science')),
        ('msc', _('Master of Science')),
        ('be', _('Bachelor of Engineering')),
        ('msceng', _('Master of Science in Engineering')),
    )

    name_en = models.CharField(
        max_length=255,
        verbose_name=_('English program name'),
        help_text=_('Enter the name of the study program'),
        blank=False,
    )

    name_sv = models.CharField(
        max_length=255,
        verbose_name=_('Swedish program name'),
        help_text=_('Enter the name of the study program'),
        blank=False,
    )

    name = TranslatedField('name_en', 'name_sv')

    degree = models.CharField(
        max_length=20,
        choices=DEGREE_CHOICES,
        verbose_name=_('Degree type'),
        blank=True,
    )

    def __str__(self) -> str:
        if self.degree:
            return _('%(degree_type)s in %(study_program)s') % {
                'degree_type': self.get_degree_display(),
                'study_program': self.name,
            }
        else:
            return self.name.__str__()
