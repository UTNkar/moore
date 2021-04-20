from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.translation import TranslatedField


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
