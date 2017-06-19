from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.edit_handlers import FieldPanel, TabbedInterface, \
    ObjectList
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from utils.translation import TranslatedField


class NewsIndexPage(Page):
    title_sv = models.CharField(max_length=255)
    translated_title = TranslatedField('title', 'title_sv')

    # Editor panels configuration
    content_panels = Page.content_panels + [
        FieldPanel('title_sv', classname="full title"),
    ]

    # Sub-page type rules
    subpage_types = ['news.NewsPage']

    def get_context(self, request, **kwargs):
        context = super(NewsIndexPage, self).get_context(request, **kwargs)

        # Add extra variables and return the updated context
        context['news_items'] = NewsPage.objects.child_of(self).live()
        return context


class NewsPage(Page):
    title_sv = models.CharField(max_length=255)
    translated_title = TranslatedField('title', 'title_sv')

    body_en = RichTextField()
    body_sv = RichTextField()
    body = TranslatedField('body_en', 'body_sv')

    created = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        verbose_name=_('Modified at'),
        auto_now=True,
    )

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField('title_sv'),
        index.SearchField('body_en'),
        index.SearchField('body_sv'),
        index.FilterField('created'),
        index.FilterField('modified'),
    ]

    # Editor panels configuration
    content_panels = Page.content_panels + [
        FieldPanel('body_en', classname="full"),
    ]
    content_panels_sv = [
        FieldPanel('title_sv', classname="full title"),
        FieldPanel('body_sv', classname="full"),
    ]
    promote_panels = [
        ImageChooserPanel('feed_image')
    ] + Page.promote_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=_('English')),
        ObjectList(content_panels_sv, heading=_('Swedish')),
        ObjectList(promote_panels, heading=_('Promote')),
        ObjectList(Page.settings_panels, heading=_('Settings')),
    ])

    # Parent page / sub-page type rules
    parent_page_types = ['news.NewsIndexPage']
    subpage_types = []
