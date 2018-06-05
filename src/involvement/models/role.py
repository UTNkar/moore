from datetime import date
from django.apps import apps
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, \
    FieldRowPanel
from utils.translation import TranslatedField


class Role(models.Model):
    """
    This class represents a role within a team or UTN
    """

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        default_permissions = ()

    team = models.ForeignKey(
        'Team',
        related_name='roles',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    official = models.BooleanField(
        verbose_name=_('Official'),
        help_text=_('This is an official role'),
        default=False,
    )

    # Display position in selection?
    archived = models.BooleanField(
        verbose_name=_('Archived'),
        help_text=_('Hide the role from menus'),
        default=False,
    )

    # ---- General Information ------

    name_en = models.CharField(
        max_length=255,
        verbose_name=_('English role name'),
        help_text=_('Enter the name of the role'),
        blank=False,
    )

    name_sv = models.CharField(
        max_length=255,
        verbose_name=_('Swedish role name'),
        help_text=_('Enter the name of the role'),
        blank=False,
    )

    name = TranslatedField('name_en', 'name_sv')

    description_en = models.TextField(
        verbose_name=_('English role description'),
        help_text=_('Enter a description of the role'),
        blank=True,
    )

    description_sv = models.TextField(
        verbose_name=_('Swedish role description'),
        help_text=_('Enter a description of the role'),
        blank=True,
    )

    description = TranslatedField('description_en', 'description_sv')

    election_email = models.EmailField(
        verbose_name=_('Election contact email address'),
        help_text=_('The email address to contact for more information '
                    'regarding the role.'),
        blank=False,
        default='styrelsen@utn.se',
    )

    def in_role(self):
        member_model = apps.get_model(settings.AUTH_USER_MODEL)
        return member_model.objects.filter(
            application__position__role=self,
            application__status='appointed',
            application__position__term_from__lte=date.today(),
            application__position__term_to__gte=date.today(),
        )

    def __str__(self) -> str:
        if self.team:
            return _('%(role)s in %(team)s') % {
                'role': self.name,
                'team': self.team,
            }
        else:
            return self.name

    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
        FieldPanel('team'),
        FieldRowPanel([
            FieldPanel('name_en'),
            FieldPanel('name_sv'),
        ]),
        FieldPanel('election_email'),
        FieldPanel('description_en'),
        FieldPanel('description_sv'),
        FieldRowPanel([
            FieldPanel('archived'),
            FieldPanel('official'),
        ]),
    ])]
