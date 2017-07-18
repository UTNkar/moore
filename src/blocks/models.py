from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

from django.utils.translation import ugettext_lazy as _

BASIC_BLOCKTYPES = [
    ('paragraph', blocks.RichTextBlock(
        template='blocks/paragraph.html',
        group=_('Basic'),
    )),
    ('image', ImageChooserBlock(
        template='blocks/image.html',
        group=_('Basic'),
    )),
]


class ColumnBlock(blocks.StructBlock):
    columns = blocks.ListBlock(blocks.StructBlock([
        ('width', blocks.IntegerBlock(
            min_value=1,
            max_value=12,
            help_text=_('Width out of 12'),
        )),
        ('content', blocks.StreamBlock(BASIC_BLOCKTYPES))
    ]))

    class Meta:
        label = _('Columns')
        icon = 'fa-columns'
        template = 'blocks/columns.html'
        group = _('Meta')


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
        label = _('Counters')
        icon = 'fa-balance-scale'
        template = 'blocks/counter.html'
        group = _('Noyce')


class HeadingBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    subtitle = blocks.CharBlock(required=False)

    class Meta:
        label = _('Heading')
        icon = 'fa-header'
        template = 'blocks/title.html'
        group = _('Basic')


class ImageDescriptionBlock(blocks.StructBlock):
    description = blocks.RichTextBlock()
    image = ImageChooserBlock()
    image_alignment = blocks.ChoiceBlock(choices=[
        ('left', _('Left')),
        ('right', _('Right')),
    ])
    hide_on_med = blocks.BooleanBlock(required=False)

    class Meta:
        label = _('Image + Description')
        icon = 'fa-file-image-o '
        template = 'blocks/image_description.html'
        group = _('Noyce')


class ImageIconsBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    image = ImageChooserBlock()
    image_alignment = blocks.ChoiceBlock(choices=[
        ('left', _('Left')),
        ('right', _('Right')),
    ])
    icons = blocks.ListBlock(blocks.StructBlock([
        ('icon', blocks.CharBlock(
            help_text=_('Material icon font icon text, as found on: '
                        'https://material.io/icons'),
        )),
        ('title', blocks.CharBlock()),
        ('description', blocks.CharBlock())
    ]))
    hide_on_med = blocks.BooleanBlock(required=False)

    class Meta:
        label = _('Image + Icons')
        icon = 'fa-file-excel-o'
        template = 'blocks/image_icons.html'
        group = _('Noyce')


class OverlayBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock(required=False)
    description = blocks.CharBlock(required=False)

    link = blocks.URLBlock(required=False)
    button = blocks.CharBlock(required=False)

    class Meta:
        label = _('Image overlay')
        icon = 'fa-clone'
        template = 'blocks/overlay.html'
        group = _('Noyce')


class PersonBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    name = blocks.CharBlock()
    role = blocks.CharBlock(required=False)
    description = blocks.RichTextBlock(required=False)
    email = blocks.EmailBlock(required=False)

    class Meta:
        label = _('Person')
        icon = 'user'
        template = 'blocks/person.html'
        group = _('Meta')


WAGTAIL_STATIC_BLOCKTYPES = BASIC_BLOCKTYPES + [
    ('heading', HeadingBlock()),  # TODO: Do we use this one?
    ('image_description', ImageIconsBlock()),
    ('image_icons', ImageDescriptionBlock()),
    ('overlay', OverlayBlock()),
    ('logos', blocks.ListBlock(
        ImageChooserBlock(),
        icon='fa-pied-piper',
        template='blocks/logos.html',
        label=_('Logos'),
        group=_('Noyce'),
    )),
    ('counters', CountersBlock()),
    ('columns', ColumnBlock()),
    ('person', PersonBlock()),
]
