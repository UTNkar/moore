from datetime import date
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, \
    FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from utils.translation import TranslatedField


class Team(models.Model):
    """This class represents a working group within UTN"""

    class Meta:
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')
        default_permissions = ()

    # ---- General Information ------
    name_en = models.CharField(
        max_length=255,
        verbose_name=_('English team name'),
        help_text=_('Enter the name of the team'),
        blank=False,
    )

    name_sv = models.CharField(
        max_length=255,
        verbose_name=_('Swedish team name'),
        help_text=_('Enter the name of the team'),
        blank=False,
    )

    name = TranslatedField('name_en', 'name_sv')

    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    description_en = models.TextField(
        verbose_name=_('English team description'),
        help_text=_('Enter a description of the team'),
        blank=True,
    )

    description_sv = models.TextField(
        verbose_name=_('Swedish team description'),
        help_text=_('Enter a description of the team'),
        blank=True,
    )

    description = TranslatedField('description_en', 'description_sv')

    def __str__(self) -> str:
        return '{}'.format(self.name)

    def get_members(self):
        return get_user_model().objects.filter(
            application__position__role__team=self,
            application__position__term_from__lte=date.today(),
            application__position__term_to__gte=date.today(),
            application__status='appointed',
        )

    def get_manual_members(self):
        members = self.get_members().values('pk')
        return get_user_model().objects.filter(
            groups=self.group
        ).exclude(
            pk__in=members
        )

    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('name_en'),
            FieldPanel('name_sv'),
        ]),
        ImageChooserPanel('logo'),
        FieldPanel('description_en'),
        FieldPanel('description_sv'),
    ])]
