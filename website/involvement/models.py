from datetime import date

from django import forms
from django.conf import settings
from django.contrib.auth.models import Group
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel, FieldPanel, \
    InlinePanel, FieldRowPanel
from wagtail.wagtailcore.models import Orderable, Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from utils.translation import TranslatedField


class RecruitmentPage(RoutablePageMixin, Page):
    # ---- General Page information ------
    title_sv = models.CharField(max_length=255)
    translated_title = TranslatedField('title', 'title_sv')

    # ------ Team selection ------
    included_teams = ParentalManyToManyField(
        'Team',
        verbose_name=_('Included teams'),
        help_text=_('Choose teams to include on the page'),
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


class Team(models.Model):
    """This class represents a working group within UTN"""

    class Meta:
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

    # ---- Contact Information ------
    leader_en = models.CharField(
        max_length=255,
        verbose_name=_('English team leader position name'),
        help_text=_('Enter the name of position of the team leader'),
        blank=True,
    )

    leader_sv = models.CharField(
        max_length=255,
        verbose_name=_('Swedish team leader position name'),
        help_text=_('Enter the name of position of the team leader'),
        blank=True,
    )

    leader = TranslatedField('leader_en', 'leader_sv')

    email = models.EmailField(
        verbose_name=_('Contact e-mail address'),
        blank=True,
    )

    def __str__(self) -> str:
        return '{}'.format(self.name)

    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('name_en'),
            FieldPanel('name_sv'),
        ]),
        FieldPanel('group'),
        ImageChooserPanel('logo'),
        FieldRowPanel([
            FieldPanel('leader_en'),
            FieldPanel('leader_sv'),
        ]),
        FieldPanel('email'),
        FieldPanel('description_en'),
        FieldPanel('description_sv'),
    ])]


def official_of(user, pk=False):
    # TODO : Is this efficient?
    applications = Application.objects.filter(
        applicant=user,
        status='appointed',
        position__term_from__lte=date.today(),
        position__term_to__gte=date.today(),
        position__role__official=True,
        position__role__team_id__isnull=False,
    ).select_related('position__role__team')
    teams = []
    for i in applications:
        if pk:
            teams.append(i.position.role.team.pk)
        else:
            teams.append(i.position.role.team)

    return teams


def member_of(user, pk=False):
    groups = user.groups.all()
    teams = []
    for group in groups:
        if hasattr(group, 'team'):
            if pk:
                teams.append(group.team.pk)
            else:
                teams.append(group.team)
    return teams


class Role(models.Model):
    """
    This class represents a role within a team or UTN
    """

    class Meta:
        verbose_name_plural = _('Roles')
        default_permissions = ()

    team = models.ForeignKey(
        Team,
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

    def __str__(self) -> str:
        return _('{} in {}').format(self.name, self.team)

    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
        FieldPanel('team'),
        FieldRowPanel([
            FieldPanel('name_en'),
            FieldPanel('name_sv'),
        ]),
        FieldPanel('description_en'),
        FieldPanel('description_sv'),
        FieldRowPanel([
            FieldPanel('archived'),
            FieldPanel('official'),
        ]),
    ])]


class Position(models.Model):
    """Position represents the execution of a role within UTN"""

    class Meta:
        verbose_name_plural = _('Positions')
        default_permissions = ()

    role = models.ForeignKey(
        Role,
        related_name='positions',
        on_delete=models.PROTECT,
        blank=False,
    )

    approval_committee = models.ForeignKey(
        Team,
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
        return "{} {}".format(self.role.name, self.term_from.year)

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


class Application(ClusterableModel):
    """An application is made to strive to acquire an position"""

    position = models.ForeignKey(
        Position,
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
        help_text=_('Present yourself and state why you are what we are '
                    'looking for'),
        blank=True,
    )
    qualifications = models.TextField(
        verbose_name=_('Qualifications'),
        help_text=_('Give a summary of relevant qualifications'),
        blank=True,
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


class Reference(Orderable):
    """Reference represents a reference given in an application"""

    application = ParentalKey(
        Application,
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
        verbose_name=_('E-mail address'),
        help_text=_('Enter an e-mail address on which your reference in '
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
