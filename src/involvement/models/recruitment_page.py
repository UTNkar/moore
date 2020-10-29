from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalManyToManyField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from utils.translation import TranslatedField
from involvement.models import Position


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

    @route(r'^my_mandates/$')
    def my_mandates(self, request):
        """View redirect for the mandate histories by user"""
        from involvement import views
        return views.my_mandates(request, self.get_context(request))

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
