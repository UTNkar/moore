from __future__ import absolute_import, unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, \
        TabbedInterface, ObjectList
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.core.blocks import RawHTMLBlock
from blocks.models import WAGTAIL_STATIC_BLOCKTYPES, EventbriteBlock
from google.models import GoogleFormBlock, GoogleDriveBlock, \
    GoogleCalendarBlock
from news.models import LatestNewsBlock
from utils.translation import TranslatedField


class WebPage(Page):
    # ---- General Page information ------

    title_sv = models.CharField(max_length=255)
    translated_title = TranslatedField('title', 'title_sv')

    body_en = StreamField(
        WAGTAIL_STATIC_BLOCKTYPES + [
            ('google_calendar', GoogleCalendarBlock()),
            ('google_drive', GoogleDriveBlock()),
            ('google_form', GoogleFormBlock()),
            ('news', LatestNewsBlock()),
            ('html', RawHTMLBlock(group="Basic")),
	    ('eventbrite', EventbriteBlock()),
        ],
        blank=True,
    )
    body_sv = StreamField(
        WAGTAIL_STATIC_BLOCKTYPES + [
            ('google_calendar', GoogleCalendarBlock()),
            ('google_drive', GoogleDriveBlock()),
            ('google_form', GoogleFormBlock()),
            ('news', LatestNewsBlock()),
            ('html', RawHTMLBlock(group="Basic")),
	    ('eventbrite', EventbriteBlock())
        ],
        blank=True,
    )
    body = TranslatedField('body_en', 'body_sv')

    content_panels_en = Page.content_panels + [
        StreamFieldPanel('body_en'),
    ]

    content_panels_sv = [
        FieldPanel('title_sv', classname="full title"),
        StreamFieldPanel('body_sv'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels_en, heading=_('English')),
        ObjectList(content_panels_sv, heading=_('Swedish')),
        ObjectList(Page.promote_panels, heading=_('Promote')),
        ObjectList(Page.settings_panels, heading=_('Settings')),
    ])
