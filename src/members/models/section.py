from django.db import models
from django.db.models import ManyToManyField
from django.utils.translation import ugettext_lazy as _
from utils.translation import TranslatedField


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
