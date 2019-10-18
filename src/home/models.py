from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import InlinePanel, MultiFieldPanel, \
    FieldRowPanel, FieldPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailforms.models import AbstractEmailForm, AbstractFormField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from blocks.models import WAGTAIL_STATIC_BLOCKTYPES, EventbriteBlock
from google.models import GoogleFormBlock, GoogleDriveBlock, \
    GoogleCalendarBlock
from involvement.models import ContactCardBlock
from news.models import LatestNewsBlock
from utils.translation import TranslatedField


class ContactPage(Page):
    # ---- General Page information ------
    title_sv = models.CharField(max_length=255)
    translated_title = TranslatedField('title', 'title_sv')

    contact_point = StreamField(
        [('person', ContactCardBlock())],
    )

    other_contacts = StreamField(
        [('contact', blocks.StructBlock([
            ('person', ContactCardBlock()),
            ('english_groups', blocks.CharBlock(
                help_text=_('Comma separated list of English group names.'),
                required=False,
            )),
            ('swedish_groups', blocks.CharBlock(
                help_text=_('Comma separated list of Swedish group names.'),
                required=False,
            )),
        ], icon='user'))],
    )

    map_location = models.CharField(
        max_length=255,
        verbose_name=_('Map Location'),
        help_text=_('Enter comma separated coordinates'),
        blank=True,
    )

    location_description = RichTextField(
        verbose_name=_('Location Description'),
        help_text=_('Enter the text to show on the map'),
        blank=True,
    )

    def get_context(self, request, *args, **kwargs):
        contacts = {}
        for contact in self.other_contacts:
            if request.LANGUAGE_CODE == 'sv':
                groups = contact.value.get('swedish_groups', '')
            else:
                groups = contact.value.get('english_groups', '')
            groups = groups.split(',')

            for group in groups:
                group = group.strip()
                list = contacts.get(group, [])
                list.append(contact.value['person'])
                contacts[group] = list

        context = super(ContactPage, self).get_context(
            request, *args, **kwargs
        )
        context['contacts'] = contacts
        return context

    content_panels = Page.content_panels + [
        FieldPanel('title_sv', classname="full title"),
        FieldPanel('map_location'),
        FieldPanel('location_description'),
        StreamFieldPanel('contact_point'),
        StreamFieldPanel('other_contacts'),
    ]


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


class FormPage(AbstractEmailForm):
    title_sv = models.CharField(max_length=255)
    translated_title = TranslatedField('title', 'title_sv')

    intro_en = StreamField(
        WAGTAIL_STATIC_BLOCKTYPES + [
            ('contact_card', ContactCardBlock()),
        ],
        verbose_name=_('English Introduction'),
        blank=True,
    )
    intro_sv = StreamField(
        WAGTAIL_STATIC_BLOCKTYPES + [
            ('contact_card', ContactCardBlock()),
        ],
        verbose_name=_('Swedish Introduction'),
        blank=True,
    )
    intro = TranslatedField('intro_en', 'intro_sv')

    thank_you_text_en = StreamField(
        WAGTAIL_STATIC_BLOCKTYPES + [
            ('contact_card', ContactCardBlock()),
        ],
        verbose_name=_('English Thank You Text'),
        blank=True,
    )
    thank_you_text_sv = StreamField(
        WAGTAIL_STATIC_BLOCKTYPES + [
            ('contact_card', ContactCardBlock()),
        ],
        verbose_name=_('Swedish Thank You Text'),
        blank=True,
    )
    thank_you_text = TranslatedField('thank_you_text_en', 'thank_you_text_sv')

    form_title_en = models.CharField(
        verbose_name=_('English Form Title'),
        max_length=255,
        blank=True
    )
    form_title_sv = models.CharField(
        verbose_name=_('Swedish Form Title'),
        max_length=255,
        blank=True,
    )
    form_title = TranslatedField('form_title_en', 'form_title_sv')

    general_panels = [
        InlinePanel('form_fields', label="Form fields"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    content_panels_en = AbstractEmailForm.content_panels + [
        StreamFieldPanel('intro_en'),
        FieldPanel('form_title_en', classname="full title"),
        StreamFieldPanel('thank_you_text_en'),
    ]

    content_panels_sv = [
        FieldPanel('title_sv', classname="full title"),
        StreamFieldPanel('intro_sv'),
        FieldPanel('form_title_sv', classname="full title"),
        StreamFieldPanel('thank_you_text_sv'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_panels, heading=_('General')),
        ObjectList(content_panels_en, heading=_('English')),
        ObjectList(content_panels_sv, heading=_('Swedish')),
        ObjectList(Page.promote_panels, heading=_('Promote')),
        ObjectList(Page.settings_panels, heading=_('Settings')),
    ])


class HomePage(Page):
    # ---- General Page information ------
    title_sv = models.CharField(max_length=255)
    translated_title = TranslatedField('title', 'title_sv')
    show_searchbar = models.BooleanField(default=True)

    body_en = StreamField(
        WAGTAIL_STATIC_BLOCKTYPES
        + [('news', LatestNewsBlock())],
        blank=True,
    )
    body_sv = StreamField(
        WAGTAIL_STATIC_BLOCKTYPES
        + [('news', LatestNewsBlock())],
        blank=True,
    )
    body = TranslatedField('body_en', 'body_sv')

    banner_panels = [InlinePanel('banners', label=_('Banner'))]

    content_panels_en = Page.content_panels + [
        StreamFieldPanel('body_en'),
    ]

    content_panels_sv = [
        FieldPanel('title_sv', classname="full title"),
        StreamFieldPanel('body_sv'),
    ]

    custom_settings_panel = Page.settings_panels + [
        MultiFieldPanel([
            FieldPanel('show_searchbar')
        ], 'Searchbar settings')
    ]

    edit_handler = TabbedInterface([
        ObjectList(banner_panels, heading=_('Banners')),
        ObjectList(content_panels_en, heading=_('English')),
        ObjectList(content_panels_sv, heading=_('Swedish')),
        ObjectList(Page.promote_panels, heading=_('Promote')),
        ObjectList(custom_settings_panel, heading=_('Settings')),
    ])


class Banner(Orderable):
    page = ParentalKey(
        HomePage,
        related_name='banners',
        on_delete=models.CASCADE,
        blank=False,
    )

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    title_en = models.CharField(
        max_length=255,
        verbose_name=_('English banner title'),
        help_text=_('Enter the title to be shown on the banner.'),
        blank=True,
    )

    title_sv = models.CharField(
        max_length=255,
        verbose_name=_('Swedish banner title'),
        help_text=_('Enter the title to be shown on the banner.'),
        blank=True,
    )

    title = TranslatedField('title_en', 'title_sv')

    text_en = models.TextField(
        verbose_name=_('English banner text'),
        help_text=_('Enter a text to be shown on the banner.'),
        blank=True,
    )

    text_sv = models.TextField(
        verbose_name=_('Swedish banner text'),
        help_text=_('Enter a text to be shown on the banner.'),
        blank=True,
    )

    text = TranslatedField('text_en', 'text_sv')

    link = models.URLField(
        verbose_name=_('Button URL'),
        blank=True,
    )

    button_en = models.TextField(
        verbose_name=_('English button text'),
        help_text=_('Enter the text to be displayed on the button.'),
        blank=True,
    )

    button_sv = models.TextField(
        verbose_name=_('Swedish button text'),
        help_text=_('Enter the text to be displayed on the button.'),
        blank=True,
    )

    button = TranslatedField('button_en', 'button_sv')

    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
        ImageChooserPanel('image'),
        FieldRowPanel([
            FieldPanel('title_en'),
            FieldPanel('title_sv'),
        ]),
        FieldPanel('text_en'),
        FieldPanel('text_sv'),
        FieldPanel('link'),
        FieldRowPanel([
            FieldPanel('button_en'),
            FieldPanel('button_sv'),
        ]),
    ])]


class WebPage(Page):
    # ---- General Page information ------
    title_sv = models.CharField(max_length=255)
    translated_title = TranslatedField('title', 'title_sv')

    body_en = StreamField(
        WAGTAIL_STATIC_BLOCKTYPES + [
            ('contact_card', ContactCardBlock()),
            ('google_calendar', GoogleCalendarBlock()),
            ('google_drive', GoogleDriveBlock()),
            ('google_form', GoogleFormBlock()),
            ('news', LatestNewsBlock()),
            ('raw_html', blocks.RawHTMLBlock(group="Basic")),
            ('eventbrite', EventbriteBlock()),
        ],
        blank=True,
    )
    body_sv = StreamField(
        WAGTAIL_STATIC_BLOCKTYPES + [
            ('contact_card', ContactCardBlock()),
            ('google_calendar', GoogleCalendarBlock()),
            ('google_drive', GoogleDriveBlock()),
            ('google_form', GoogleFormBlock()),
            ('news', LatestNewsBlock()),
            ('raw_html', blocks.RawHTMLBlock(group="Basic")),
            ('eventbrite', EventbriteBlock()),
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
