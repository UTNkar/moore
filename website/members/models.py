import requests
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from requests.auth import HTTPDigestAuth
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

from utils.translation import TranslatedField


class StudyProgram(models.Model):
    """This class describes a university study program"""

    class Meta:
        verbose_name = _('study program')
        verbose_name_plural = _('study programs')

    DEGREE_CHOICES = (
        ('bachelor', _('Bachelor\'s Degree')),
        ('master', _('Master\'s Degree')),
        ('engineer', _('Engineer\'s Degree')),
    )

    name_en = models.CharField(
        max_length=255,
        verbose_name=_('English program name'),
        help_text=_('Enter the name of the study program'),
        null=False,
        blank=False,
    )

    name_sv = models.CharField(
        max_length=255,
        verbose_name=_('Swedish program name'),
        help_text=_('Enter the name of the study program'),
        null=False,
        blank=False,
    )

    name = TranslatedField('name_en', 'name_sv')

    abbreviation_en = models.CharField(
        max_length=130,
        verbose_name=_('English program abbreviation'),
        help_text=_('Enter the abbreviation for the study program'),
        null=True,
        blank=True,
    )

    abbreviation_sv = models.CharField(
        max_length=130,
        verbose_name=_('Swedish program abbreviation'),
        help_text=_('Enter the abbreviation for the study program'),
        null=True,
        blank=True,
    )

    abbreviation = TranslatedField('name_en', 'name_sv')

    degree = models.CharField(
        max_length=20,
        choices=DEGREE_CHOICES,
        verbose_name=_('Degree type'),
        blank=False,
        null=False,
    )

    def __str__(self) -> str:
        return '%s in %s' % (self.get_degree_display(), self.name)


class Member(SimpleEmailConfirmationUserMixin, AbstractUser):
    """This class describes a member"""

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
        null=True,
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
        null=False,
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
        null=True,
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
        null=True,
        blank=True,
    )

    study = models.ForeignKey(
        StudyProgram,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return '%s %s' % (self.first_name, self.last_name)
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
            r = requests.get(
                'https://register.utn.se/api.php',
                auth=HTTPDigestAuth(settings.MEMBERSHIP_API_USER,
                                    settings.MEMBERSHIP_API_PASSWORD),
                params={
                    'action': 'check',
                    'person_number': self.person_number().replace('-', '')
                },
            )
            try:
                data = r.json().get('status')
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
