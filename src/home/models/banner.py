from __future__ import absolute_import, unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldRowPanel, \
        FieldPanel
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from utils.translation import TranslatedField

from wagtailmedia.edit_handlers import MediaChooserPanel


from wagtail.core import hooks


@hooks.register('construct_media_chooser_queryset')
def show_my_uploaded_media_only(media, request):
    # Only show video media
    return media.filter(type="video")


class Banner(Orderable):
    page = ParentalKey(
        'HomePage',
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

    video = models.ForeignKey(
        'wagtailmedia.Media',
        help_text=_("""Banner video media. If video is not supported by the
        browser, the image is shown instead."""),
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
        MediaChooserPanel('video'),
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
