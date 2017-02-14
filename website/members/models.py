from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.translation import TranslatedField


class StudyProgram(models.Model):
    """This class describes a university study program"""

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


class Member(AbstractUser):
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

    def person_number(self) -> str:
        return '%s-%s' % (self.birthday.strftime('%Y%m%d'),
                          self.person_number_ext)
