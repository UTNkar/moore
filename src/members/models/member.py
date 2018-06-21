import requests
from datetime import date
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager, \
        PermissionsMixin
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from requests.auth import HTTPDigestAuth
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin


class CaseInsensitiveUsernameUserManager(UserManager):
    # Get username by insensitive case
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact' \
            .format(self.model.USERNAME_FIELD)
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


    @property
    def teams(self):
        Team = apps.get_model('involvement', 'Team')
        groups = self.groups.all()
        return Team.objects.filter(
            models.Q(
                roles__positions__term_from__lte=date.today(),
                roles__positions__term_to__gte=date.today(),
                roles__positions__applications__applicant=self,
                roles__positions__applications__status='appointed',
             ) |
            models.Q(roles__group__in=groups)
        )

    @property
    def roles(self):
        Role = apps.get_model('involvement', 'Role')
        groups = self.groups.all()
        return Role.objects.filter(
            models.Q(
                positions__term_from__lte=date.today(),
                positions__term_to__gte=date.today(),
                positions__applications__applicant=self,
                positions__applications__status='appointed',
             ) |
            models.Q(group__in=groups)
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

    # def has_perm(self, perm, obj=None):
    #     if obj is not None:
    #         return super(Member, self).has_perm(perm, obj)

    #     if super(Member, self).has_perm(perm):
    #         return True

    #     app_label, codename = perm.split('.')
    #     return super(Member, self).has_perm(perm) \
    #         or self.roles.filter(
    #             group__permissions__codename=codename,
    #             group__permissions__content_type__app_label=app_label).exists()

