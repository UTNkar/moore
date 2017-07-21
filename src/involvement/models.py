from datetime import date

from django import forms
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel, FieldPanel, \
    InlinePanel, FieldRowPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.blocks import SnippetChooserBlock
from wagtail.wagtailsnippets.models import register_snippet

from utils.translation import TranslatedField


class Application(ClusterableModel):
    """An application is made to strive to acquire an position"""

    position = models.ForeignKey(
        'Position',
        related_name='applications',
        on_delete=models.PROTECT,
        blank=False,
    )

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=False,
    )

    class Meta:
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')
        unique_together = ('position', 'applicant')
        default_permissions = ()

    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('submitted', _('Submitted')),
        ('approved', _('Approved')),
        ('disapproved', _('Disapproved')),
        ('appointed', _('Appointed')),
        ('turned_down', _('Turned down')),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name=_('Status'),
        blank=False,
        null=False,
    )

    # ---- Application Information ------
    cover_letter = models.TextField(
        verbose_name=_('Cover Letter'),
        help_text=_('Present yourself and state why you are who we are '
                    'looking for'),
        blank=True,
    )
    qualifications = models.TextField(
        verbose_name=_('Qualifications'),
        help_text=_('Give a summary of relevant qualifications'),
        blank=True,
    )

    # Access overhead
    removed = models.BooleanField(
        default=False,
    )

    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('applicant'),
            FieldPanel('position'),
        ]),
        FieldPanel('cover_letter'),
        FieldPanel('qualifications'),
        InlinePanel('references'),
        FieldPanel('status'),
    ])]


class Position(models.Model):
    """Position represents the execution of a role within UTN"""

    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')
        default_permissions = ()

    role = models.ForeignKey(
        'Role',
        related_name='positions',
        on_delete=models.PROTECT,
        blank=False,
    )

    approval_committee = models.ForeignKey(
        'Team',
        verbose_name=_('Approval committee'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    recruitment_start = models.DateField(
        verbose_name=_('Start of recruitment'),
        default=date.today,
    )
    recruitment_end = models.DateField(verbose_name=_('Recruitment deadline'))

    # ---- Appointment Information ------
    appointments = models.IntegerField(
        verbose_name=_('Number of appointments'),
        help_text=_('Enter the number of concurrent appointments to the '
                    'position'),
        default=1,
    )

    term_from = models.DateField(verbose_name=_('Date of appointment'))

    term_to = models.DateField(verbose_name=_('End date of appointment'))

    comment_en = models.TextField(
        verbose_name=_('English extra comments'),
        help_text=_('Enter extra comments specific to the position this '
                    'year.'),
        blank=True,
    )

    comment_sv = models.TextField(
        verbose_name=_('Swedish extra comments'),
        help_text=_('Enter extra comments specific to the position this '
                    'year.'),
        blank=True,
    )

    comment = TranslatedField('comment_en', 'comment_sv')

    def __str__(self) -> str:
        if self.term_from.year != self.term_to.year:
            return "%s %s-%s" \
                   % (self.role.name, self.term_from.year, self.term_to.year)
        else:
            return "%s %s" % (self.role.name, self.term_from.year)

    @property
    def is_past_due(self):
        return date.today() > self.recruitment_end

    def current_action(self) -> str:
        if self.is_past_due:
            applications = self.applications.exclude(status='draft')
            if applications.all().filter(status='submitted').exists() \
                    and self.approval_committee is not None:
                return 'approve'
            elif applications.all().filter(status='appointed') \
                    .count() >= self.appointments:
                return 'done'
            else:
                return 'appoint'
        else:
            return 'recruit'

    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('role'),
            FieldPanel('appointments'),
        ]),
        FieldRowPanel([
            FieldPanel('term_from'),
            FieldPanel('term_to'),
        ]),
        FieldPanel('approval_committee'),
        FieldRowPanel([
            FieldPanel('recruitment_start'),
            FieldPanel('recruitment_end'),
        ]),
        FieldPanel('comment_en'),
        FieldPanel('comment_sv'),
    ])]


class RecruitmentPage(RoutablePageMixin, Page):
    # ---- General Page information ------
    title_sv = models.CharField(max_length=255)
    translated_title = TranslatedField('title', 'title_sv')

    # ------ Team selection ------
    included_teams = ParentalManyToManyField(
        'Team',
        verbose_name=_('Included teams'),
        help_text=_('Choose teams to include on the page. This overrules'
                    'excluded teams'),
        related_name='include_on_page',
        blank=True,
    )
    excluded_teams = ParentalManyToManyField(
        'Team',
        verbose_name=_('Excluded teams'),
        help_text=_('Choose teams to exclude from the page'),
        related_name='exclude_on_page',
        blank=True,
    )

    # ------ Methods ------
    def get_context(self, request, *args, **kwargs):
        context = super(RecruitmentPage, self).get_context(
            request, *args, **kwargs
        )
        context['positions'] = Position.objects.all()
        if self.included_teams.all():
            context['positions'] = context['positions'].filter(
                role__team__in=self.included_teams.all()
            )
        elif self.excluded_teams.all():
            context['positions'] = context['positions'].exclude(
                role__team__in=self.excluded_teams.all()
            )
        return context

    # ------ Routing ------
    @route(r'^$')
    def open_positions(self, request):
        """View redirect for the currently open positions"""
        from involvement import views
        return views.open_positions(request, self.get_context(request))

    @route(r'^my_applications/$')
    def my_applications(self, request):
        """View redirect for the applications by user"""
        from involvement import views
        return views.my_applications(request, self.get_context(request))

    @route(r'^position/(\d+)/$')
    def position(self, request, position=None):
        """
        View redirect for a specific position.
        """
        from involvement import views
        return views.view_position(request, self.get_context(request), self,
                                   position)

    # ------ Administrator settings ------
    content_panels = Page.content_panels + [
        FieldPanel('title_sv'),
        FieldPanel('included_teams', widget=forms.CheckboxSelectMultiple),
        FieldPanel('excluded_teams', widget=forms.CheckboxSelectMultiple),
    ]
    # Don't allow any sub pages
    subpage_types = []


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


class Team(models.Model):
    """This class represents a working group within UTN"""

    class Meta:
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')
        default_permissions = ()
        permissions = (
            ('admin', _('Can administrate the recruitment process')),
        )

    group = models.OneToOneField(
        Group,
        on_delete=models.PROTECT,
    )

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
        FieldPanel('group'),
        ImageChooserPanel('logo'),
        FieldPanel('description_en'),
        FieldPanel('description_sv'),
    ])]


class Reference(Orderable):
    """Reference represents a reference given in an application"""

    application = ParentalKey(
        'Application',
        related_name='references',
        on_delete=models.CASCADE,
        blank=False,
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        help_text=_('Enter the name of your reference'),
        blank=False,
    )

    position = models.CharField(
        max_length=255,
        verbose_name=_('Position'),
        help_text=_('Enter the position in which your reference relates to '
                    'you'),
        blank=False,
    )

    email = models.EmailField(
        verbose_name=_('email address'),
        help_text=_('Enter an email address on which your reference in '
                    'reachable'),
        blank=True,
    )

    phone_number = models.CharField(
        max_length=20,
        verbose_name=_('Phone number'),
        help_text=_('Enter a valid phone number'),
        validators=[validators.RegexValidator(
            regex=r'^\+?\d+$',
            message=_('Enter a phone number on which your reference is '
                      'reachable'),
        )],
        blank=True,
    )

    comment = models.CharField(
        max_length=500,
        verbose_name=_('Comment'),
        help_text=_('Enter any additional comments regarding your reference'),
        blank=True,
    )

    def __str__(self) -> str:
        ref = '%s - %s' % (self.name, self.position)
        if self.phone_number and self.email:
            ref += '\nContact: %s or %s' % (self.phone_number, self.email)
        elif self.phone_number or self.email:
            ref += '\nContact: %s' % self.phone_number + self.email
        if self.comment:
            ref += '\nComment: %s' % self.comment

        return ref

    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('name'),
            FieldPanel('position'),
        ]),
        FieldRowPanel([
            FieldPanel('email'),
            FieldPanel('phone_number'),
        ]),
        FieldPanel('comment'),
    ])]


@register_snippet
class ContactCard(models.Model):
    role = models.OneToOneField(
        'Role',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='contact_cards',
    )
    picture = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    description_en = RichTextField(
        verbose_name=_('English Description'),
        blank=True,
    )
    description_sv = RichTextField(
        verbose_name=_('Swedish Description'),
        blank=True,
    )
    description = TranslatedField('description_en', 'description_sv')

    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
        help_text=_('Overrides account name of position holder of the selected'
                    ' role.'),
        blank=True,
    )

    role_text_en = models.CharField(
        max_length=100,
        verbose_name=_('English Role Name'),
        help_text=_('Overrides role name from the selected role.'),
        blank=True,
    )
    role_text_sv = models.CharField(
        max_length=100,
        verbose_name=_('Swedish Role Name'),
        help_text=_('Overrides role name from the selected role.'),
        blank=True,
    )
    role_text = TranslatedField('role_text_en', 'role_text_sv')

    email = models.EmailField(
        verbose_name=_('Email address'),
        help_text=_('Overrides account email address of position holder of the'
                    ' selected role.'),
        blank=True,
    )

    def __str__(self) -> str:
        if self.role:
            return self.role.__str__()
        else:
            return '%(name)s - %(role)s' % {
                'name': self.name,
                'role': self.role_text
            }

    panels = [
        FieldPanel('role'),
        ImageChooserPanel('picture'),
        FieldPanel('description_en'),
        FieldPanel('description_sv'),
        FieldPanel('name'),
        FieldPanel('role_text_en'),
        FieldPanel('role_text_sv'),
        FieldPanel('email'),
    ]


class ContactCardBlock(SnippetChooserBlock):
    def __init__(self, **kwargs):
        super(ContactCardBlock, self).__init__(
            'involvement.ContactCard', **kwargs
        )

    class Meta:
        label = _('Contact Card')
        icon = 'user'
        template = 'involvement/blocks/contact_card.html'
        group = _('Meta')


def member_of(user, pk=False):
    if user.is_anonymous:
        return []
    groups = user.groups.all()
    teams = Team.objects.filter(
        group__in=groups
    )
    if pk:
        return teams.values_list('pk', flat=True)
    else:
        return teams


def official_of(user, pk=False):
    if user.is_anonymous:
        return []
    teams = Team.objects.filter(
        roles__official=True,
        roles__positions__applications__applicant=user,
        roles__positions__applications__status='appointed',
        roles__positions__term_from__lte=date.today(),
        roles__positions__term_to__gte=date.today(),
    )
    if pk:
        return teams.values_list('pk', flat=True)
    else:
        return teams
