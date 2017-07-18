from datetime import date

from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, \
    TabbedInterface, ObjectList
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch import index

from blocks.models import WAGTAIL_STATIC_BLOCKTYPES
from utils.translation import TranslatedField


class GoogleFormBlock(blocks.StructBlock):
    form_id = blocks.CharBlock()
    height = blocks.IntegerBlock()

    class Meta:
        label = _('Google Form')
        icon = 'fa-check-square-o'
        template = 'google/blocks/form.html'
        group = _('Embed')


class GoogleFormIndex(Page):
    title_sv = models.CharField(max_length=255)
    translated_title = TranslatedField('title', 'title_sv')

    description_en = RichTextField(
        verbose_name=_('English description'),
        blank=True,
    )
    description_sv = RichTextField(
        verbose_name=_('Swedish description'),
        blank=True,
    )
    description = TranslatedField('description_en', 'description_sv')

    # Editor panels configuration
    content_panels = Page.content_panels + [
        FieldPanel('title_sv', classname="full title"),
        FieldPanel('description_en'),
        FieldPanel('description_sv'),
    ]

    # Sub-page type rules
    subpage_types = ['google.GoogleFormPage']

    def get_context(self, request, **kwargs):
        context = super(GoogleFormIndex, self).get_context(request, **kwargs)

        # Add extra variables and return the updated context
        context['google_forms'] = GoogleFormPage.objects.child_of(self).live()\
            .order_by('-deadline')
        return context


class GoogleFormPage(Page):
    title_sv = models.CharField(max_length=255)
    translated_title = TranslatedField('title', 'title_sv')

    # TODO: Limit to one form!
    form_en = StreamField([('google_form', GoogleFormBlock())])
    form_sv = StreamField([('google_form', GoogleFormBlock())])
    form = TranslatedField('form_en', 'form_sv')

    deadline = models.DateField(verbose_name=_('Form deadline'))

    results_en = StreamField(
        WAGTAIL_STATIC_BLOCKTYPES,
        blank=True,
    )
    results_sv = StreamField(
        WAGTAIL_STATIC_BLOCKTYPES,
        blank=True,
    )
    results = TranslatedField('results_en', 'results_sv')

    @property
    def is_past_due(self) -> bool:
        return date.today() > self.deadline

    # Editor panels configuration
    content_panels = Page.content_panels + [
        FieldPanel('title_sv', classname="full title"),
        FieldPanel('deadline'),
        StreamFieldPanel('form_en'),
        StreamFieldPanel('form_sv'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=_('Common')),
        ObjectList([StreamFieldPanel('results_en')], heading=_('English')),
        ObjectList([StreamFieldPanel('results_sv')], heading=_('Swedish')),
        ObjectList(
            Page.promote_panels + Page.settings_panels, heading=_('Settings')
        ),
    ])

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField('title_sv'),
        index.FilterField('results_en'),
        index.FilterField('results_sv'),
        index.FilterField('deadline'),
    ]

    # Parent page / subpage type rules
    parent_page_types = ['google.GoogleFormIndex']
    subpage_types = []


class GoogleDriveBlock(blocks.StructBlock):
    folder_id = blocks.CharBlock()
    view = blocks.ChoiceBlock(choices=[
        ('list', _('List')),
        ('grid', _('Grid')),
    ])
    height = blocks.IntegerBlock()

    class Meta:
        label = _('Google Drive')
        icon = 'fa-folder-open'
        template = 'google/blocks/drive.html'
        group = _('Embed')
