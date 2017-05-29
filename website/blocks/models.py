from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

from django.utils.translation import ugettext_lazy as _


class CountersBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    counters = blocks.ListBlock(blocks.StructBlock([
        ('icon', blocks.CharBlock(
            help_text=_('Material icon font icon text, as found on: '
                        'https://material.io/icons'),
        )),
        ('value', blocks.CharBlock()),
        ('description', blocks.CharBlock(required=False))
    ]))
    style = blocks.ChoiceBlock(choices=[
        ('light', _('Light')),
        ('dark', _('Dark')),
    ])

    class Meta:
        icon = 'fa-balance-scale'
        template = 'blocks/counter.html'


class HeadingBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.CharBlock(required=False)

    class Meta:
        icon = 'fa-header'
        template = 'blocks/title.html'


class ImageDescription(blocks.StructBlock):
    description = blocks.RichTextBlock()
    image = ImageChooserBlock()
    image_alignment = blocks.ChoiceBlock(choices=[
        ('left', _('Left')),
        ('right', _('Right')),
    ])
    hide_on_med = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'fa-picture-o'
        template = 'blocks/image_description.html'

WAGTAIL_CONTENT_BLOCKTYPES = [
    ('heading', HeadingBlock()),
    ('paragraph', blocks.RichTextBlock()),
    ('image_description', ImageDescription()),
    ('counters', CountersBlock()),
    ('image', ImageChooserBlock()),
]
