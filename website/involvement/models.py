from django import forms
from django.conf import settings
from django.core import validators
from django.db import models
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from utils.translation import TranslatedField
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import MultiFieldPanel, FieldPanel,\
    InlinePanel, FieldRowPanel
from wagtail.wagtailcore.models import Orderable, Page


class RequirementPage(RoutablePageMixin, Page):

    # ---- General Page information ------
    title_sv = models.CharField(max_length=255)
    translated_title = TranslatedField('title', 'title_sv')

    # ------ Team selection ------
    included_teams = ParentalManyToManyField(
        'Team',
        verbose_name=_('Included teams'),
        help_text=_('Select teams to include on the page'),
        related_name='include_on_page',
        blank=True,
    )
    excluded_teams = ParentalManyToManyField(
        'Team',
        verbose_name=_('Excluded teams'),
        help_text=_('Select teams to exclude from the page'),
        related_name='exclude_on_page',
        blank=True,
    )

    # ------ Routing ------
    @route(r'^$')
    def open_positions(self, request):
        """View function for the currently open positions"""
        pass

    @route(r'^sent_applications/$')
    def sent_applications(self, request):
        """View function for the sent applications by user"""
        pass

    @route(r'^action/$')
    def action_list(self, request):
        """
        View function for the applications that require (future) attention
        from the user
        """
        pass

    @route(r'^position/(\d+)/$', name='position')
    def position(self, request, position=None):
        """
        View function for a specific position.
        """
        pass

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
        FieldRowPanel([
            FieldPanel('leader_en'),
            FieldPanel('leader_sv'),
        ]),
        FieldPanel('email'),
        FieldPanel('description_en'),
        FieldPanel('description_sv'),
    ])]


class Function(models.Model):
    """
    This class represents a function held by a member within UTN or its
    committees
    """
    class Meta:
        verbose_name_plural = _('Functions')

    team = models.ForeignKey(
        Team,
        related_name='functions',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    # Display position in selection?
    archived = models.BooleanField(
        verbose_name=_('Archived'),
        help_text=_('Hide the position from menus'),
        default=False,
    )

    # ---- General Information ------

    name_en = models.CharField(
        max_length=255,
        verbose_name=_('English function name'),
        help_text=_('Enter the name of the function'),
        blank=False,
    )

    name_sv = models.CharField(
        max_length=255,
        verbose_name=_('Swedish function name'),
        help_text=_('Enter the name of the function'),
        blank=False,
    )

    name = TranslatedField('name_en', 'name_sv')

    description_en = models.TextField(
        verbose_name=_('English function description'),
        help_text=_('Enter a description of the function'),
        blank=True,
    )

    description_sv = models.TextField(
        verbose_name=_('Swedish function description'),
        help_text=_('Enter a description of the function'),
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
        FieldPanel('archived'),
    ])]


class Position(models.Model):
    """Appointment represents the holding of a function."""
    class Meta:
        verbose_name_plural = _('Positions')

    function = models.ForeignKey(
        Function,
        related_name='positions',
        on_delete=models.PROTECT,
        blank=False,
    )

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

    comment = TranslatedField('comments_en', 'comments_sv')

    def __str__(self) -> str:
        return "{} {}".format(self.function.name, self.term_from.year)

    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('function'),
            FieldPanel('appointments'),
        ]),
        FieldRowPanel([
            FieldPanel('term_from'),
            FieldPanel('term_to'),
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

    draft = models.BooleanField(
        verbose_name=_('Draft'),
        help_text=_('Save application as a draft'),
        default=False,
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
        FieldPanel('draft'),
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
