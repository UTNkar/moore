from datetime import date
from django.contrib.auth.models import Group
from django.core import validators
from django.apps import apps
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, \
    FieldRowPanel
from utils.translation import TranslatedField
from involvement.rule_utils import is_fum, is_board, is_presidium, \
    is_group_leader


class Role(models.Model):
    """
    This class represents a role within a team or UTN
    """

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        default_permissions = ()
        permissions = (
            ('admin', _('Admin')),
            ('fum', _('FUM')),
            ('board', _('Board')),
            ('presidium', _('Presidium')),
            ('group_leader', _('Group Leader')),
            ('engaged', _('Engaged')),
        )

    group = models.ForeignKey(
        Group,
        related_name='roles',
        on_delete=models.PROTECT,
    )

    team = models.ForeignKey(
        'Team',
        related_name='roles',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
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

    phone_number = models.CharField(
        max_length=20,
        verbose_name=_('Phone number'),
        help_text=_('Enter a phone number to contact this role.'),
        validators=[validators.RegexValidator(
            regex=r'^\+?\d+$',
            message=_('Please enter a valid phone number'),
        )],
        blank=True,
    )

    @property
    def contact_phone_number(self):
        """
        Returns:
            If self.phone_number is blank. Will return first occurence
            of a current position holder for this role if any,
            self.phone_number otherwise
        """
        if not self.phone_number:
            current_holder = self.in_role.first()
            if current_holder is not None:
                return current_holder.phone_number

        return self.phone_number

    def in_role(self):
        member_model = apps.get_model(settings.AUTH_USER_MODEL)
        return member_model.objects.filter(
            application__position__role=self,
            application__status='appointed',
            application__position__term_from__lte=date.today(),
            application__position__term_to__gte=date.today(),
        )

    @staticmethod
    def editable_codenames(user):
        if user.is_anonymous:
            return []

        permission_filter = []
        if is_fum(user):
            permission_filter += ['board']
        if is_board(user):
            permission_filter += ['presidium']
        if is_presidium(user):
            permission_filter += ['group_leader', 'engaged']
        if is_group_leader(user):
            permission_filter += ['engaged']

        return permission_filter

    @staticmethod
    def edit_applicant_codenames(user):
        if user.is_anonymous:
            return []

        permission_filter = []
        if is_fum(user):
            permission_filter += ['board', 'presidium']
        if is_board(user):
            permission_filter += ['presidium']
        if is_presidium(user):
            permission_filter += ['group_leader', 'engaged']
        if is_group_leader(user):
            permission_filter += ['engaged']

        return permission_filter

    @staticmethod
    def edit_permission_of(user, pk=False):
        if user.is_anonymous:
            return []

        permission_filter = Role.editable_codenames(user)
        roles = Role.objects.filter(
            group__permissions__codename__in=permission_filter
        )
        if pk:
            return roles.values_list('pk', flat=True)
        else:
            return roles

    @staticmethod
    def edit_applicant_permission_of(user, pk=False):
        if user.is_anonymous:
            return []

        permission_filter = Role.edit_applicant_codenames(user)
        roles = Role.objects.filter(
            group__permissions__codename__in=permission_filter
        )
        if pk:
            return roles.values_list('pk', flat=True)
        else:
            return roles

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
        FieldPanel('group'),
        FieldPanel('election_email'),
        FieldPanel('phone_number'),
        FieldPanel('description_en'),
        FieldPanel('description_sv'),
        FieldRowPanel([
            FieldPanel('archived'),
        ]),
    ])]
