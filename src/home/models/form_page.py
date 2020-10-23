from __future__ import absolute_import, unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import InlinePanel, MultiFieldPanel, \
    FieldRowPanel, FieldPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.contrib.forms.models import AbstractEmailForm
from blocks.models import WAGTAIL_STATIC_BLOCKTYPES
from utils.translation import TranslatedField
from involvement.blocks import ContactCardBlock
from wagtailcaptcha.models import WagtailCaptchaEmailForm


class FormPage(WagtailCaptchaEmailForm):

    title_sv = models.CharField(max_length=255)
    translated_title = TranslatedField('title', 'title_sv')
    use_recaptcha = models.BooleanField(
        default=False,
        verbose_name=_("Use Recaptcha"),
    )

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

    custom_settings_panel = Page.settings_panels + [
        MultiFieldPanel([
            FieldPanel('use_recaptcha'),
        ],  'Recaptcha')
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_panels, heading=_('General')),
        ObjectList(content_panels_en, heading=_('English')),
        ObjectList(content_panels_sv, heading=_('Swedish')),
        ObjectList(Page.promote_panels, heading=_('Promote')),
        ObjectList(custom_settings_panel, heading=_('Settings')),
    ])
