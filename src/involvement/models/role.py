from datetime import date
from django.contrib.auth.models import Group
from django.core import validators
from django.forms import CheckboxSelectMultiple
from django.apps import apps
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, \
    FieldRowPanel
from utils.translation import TranslatedField
from involvement.rule_utils import is_admin, is_board, is_fum, \
    is_group_leader, is_presidium


class Role(models.Model):
    """
    This class represents a role within a team or UTN
    """

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        default_permissions = ()

    TYPE_CHOICES = (
        ('admin', _('Admin')),
        ('fum', _('FUM')),
        ('board', _('Board')),
        ('presidium', _('Presidium')),
        ('group_leader', _('Group Leader')),
        ('engaged', _('Engaged')),
    )

    role_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name=_('Role type'),
        blank=False,
        null=False,
    )

    group = models.ForeignKey(
        Group,
        related_name='roles',
        on_delete=models.PROTECT,
    )

    teams = models.ManyToManyField(
        'Team',
        related_name='roles',
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
            current_holder = self.members.first()
            if current_holder is not None:
                return current_holder.phone_number

        return self.phone_number

    def members(self):
        member_model = apps.get_model(settings.AUTH_USER_MODEL)
        return member_model.objects.filter(
            application__position__role=self,
            application__status='appointed',
            application__position__term_from__lte=date.today(),
            application__position__term_to__gte=date.today(),
        )

    @staticmethod
    def editable_role_types(user):
        if user.is_anonymous:
            return []

        if is_admin(user):
            return ['admin', 'fum', 'board', 'presidium', 'group_leader', 'engaged']
        elif is_fum(user):
            return ['board']
        elif is_board(user):
            return ['presidium']
        elif is_presidium(user):
            return ['group_leader', 'engaged']
        elif is_group_leader(user):
            return ['engaged']

        return []

    @staticmethod
    def edit_applicant_role_types(user):
        if user.is_anonymous:
            return []

        if is_admin(user):
            return ['admin', 'fum', 'board', 'presidium', 'group_leader', 'engaged']
        elif is_fum(user):
            return ['board', 'presidium']
        elif is_board(user):
            return ['presidium']
        elif is_presidium(user):
            return ['group_leader', 'engaged']
        elif is_group_leader(user):
            return ['engaged']

        return []

    @staticmethod
    def edit_role_types_of(user, pk=False):
        if user.is_anonymous:
            return [] if pk else Role.objects.none()

        role_type_filter = Role.editable_role_types(user)
        roles = Role.objects.filter(
            role_type__in=role_type_filter
        )
        if pk:
            return roles.values_list('pk', flat=True)
        else:
            return roles

    @staticmethod
    def edit_applicant_permission_of(user, pk=False):
        if user.is_anonymous:
            return [] if pk else Role.objects.none()

        role_type_filter = Role.edit_applicant_role_types(user)
        roles = Role.objects.filter(
            role_type__in=role_type_filter
        )
        if pk:
            return roles.values_list('pk', flat=True)
        else:
            return roles

    @property
    def team_names(self):
        return ', '.join([str(i) for i in self.teams.all()])

    @property
    def team_logo(self):
        if self.teams.count():
            return self.teams.first().logo
        return None

    def __str__(self) -> str:
        if self.teams:
            return _('%(role)s in %(teams)s') % {
                'role': self.name,
                'teams': self.team_names,
            }
        else:
            return self.name

    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
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
        FieldPanel('role_type'),
        FieldPanel('teams', widget=CheckboxSelectMultiple),
    ])]
