from __future__ import absolute_import, unicode_literals
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, \
        TabbedInterface, ObjectList
from wagtail.fields import StreamField
from wagtail.models import Page
from blocks.models import WAGTAIL_STATIC_BLOCKTYPES, EventbriteBlock, \
    HTMLCodeBlock
from google.models import GoogleFormBlock, GoogleDriveBlock, \
    GoogleCalendarBlock
from events.blocks import EventListBlock
from news.models import LatestNewsBlock
from utils.translation import TranslatedField
from wagtail.api import APIField


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
            ('html', HTMLCodeBlock()),
            ('eventbrite', EventbriteBlock()),
            ('events', EventListBlock()),
        ],
        blank=True,
        use_json_field=True,
    )
    body_sv = StreamField(
        WAGTAIL_STATIC_BLOCKTYPES + [
            ('google_calendar', GoogleCalendarBlock()),
            ('google_drive', GoogleDriveBlock()),
            ('google_form', GoogleFormBlock()),
            ('news', LatestNewsBlock()),
            ('html', HTMLCodeBlock()),
            ('eventbrite', EventbriteBlock())
        ],
        blank=True,
        use_json_field=True,
    )
    body = TranslatedField('body_en', 'body_sv')

    content_panels_en = Page.content_panels + [
        FieldPanel('body_en'),
    ]

    content_panels_sv = [
        FieldPanel('title_sv', classname="full title"),
        FieldPanel('body_sv'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels_en, heading=_('English')),
        ObjectList(content_panels_sv, heading=_('Swedish')),
        ObjectList(Page.promote_panels, heading=_('Promote')),
        ObjectList(Page.settings_panels, heading=_('Settings')),
    ])

    api_fields = [
        APIField('title_sv'),
        APIField('body_en'),
        APIField('body_sv'),
    ]
