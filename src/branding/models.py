from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting

from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, \
    MultiFieldPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from utils.translation import TranslatedField


@register_setting(icon='fa-window-minimize')
class FooterSettings(BaseSetting):
    class Meta:
        verbose_name = _('footer')

    footer_en = StreamField(
        [('column', blocks.StructBlock([
            ('size', blocks.IntegerBlock(min_value=1, max_value=12)),
            ('content', blocks.RichTextBlock()),
        ]))],
        blank=True,
    )

    footer_sv = StreamField(
        [('column', blocks.StructBlock([
            ('size', blocks.IntegerBlock(min_value=1, max_value=12)),
            ('content', blocks.RichTextBlock()),
        ]))],
        blank=True,
    )

    footer = TranslatedField('footer_en', 'footer_sv')

    panels_sv = [
        StreamFieldPanel('footer_sv')
    ]

    panels_en = [
        StreamFieldPanel('footer_en')
    ]

    edit_handler = TabbedInterface([
        ObjectList(panels_en, heading=_("English")),
        ObjectList(panels_sv, heading=_("Swedish"))
    ])


@register_setting(icon='openquote')
class SocialMediaSettings(BaseSetting):
    class Meta:
        verbose_name = _('social media accounts')

    facebook = models.URLField(
        help_text=_('Your Facebook page URL'),
        blank=True,
    )
    instagram = models.CharField(
        max_length=255,
        help_text=_('Your Instagram username, without the @'),
        blank=True,
    )
    twitter = models.CharField(
        max_length=255,
        help_text=_('Your Twitter username, without the @'),
        blank=True,
    )


class Logo(models.Model):
    class Meta:
        verbose_name = _('logo')
        verbose_name_plural = _('logos')

    def __str__(self):
        logotext = str(_('logo'))
        return logotext.capitalize()

    CATEGORY_CHOICES = (
        ('committee', _('Committee')),
        ('section', _('Section')),
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name=_('category'),
        blank=False,
        null=False,
    )

    link = models.URLField(
        verbose_name=_('links to'),
        null=False,
        blank=False,
    )

    logo = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('logo'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    logo_white = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('white logo'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    logo_black = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('black logo'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    belongs_to = models.ForeignKey(
        'wagtailcore.Site',
        verbose_name=_('belongs to'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('category'),
            FieldPanel('link'),
        ]),
        ImageChooserPanel('logo'),
        ImageChooserPanel('logo_white'),
        ImageChooserPanel('logo_black'),
        FieldPanel('belongs_to'),
    ])]
