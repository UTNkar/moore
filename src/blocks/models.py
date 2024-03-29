from django.utils.translation import gettext_lazy as _
from django import forms
from wagtail.core import blocks
from wagtail.core.blocks.field_block import CharBlock, ChoiceBlock
from wagtail.images.blocks import ImageChooserBlock
from involvement.blocks import ContactCardBlock
from instagram.blocks import InstagramFeedChooserBlock
import requests
from datetime import datetime
from blocks.widgets import CodeMirrorWidget
from wagtail.core.blocks.struct_block import StructBlockAdapter
from wagtail.core.telepath import register
from django.utils.functional import cached_property


# BASIC BLOCKTYPES
class HTMLCodeBlock(blocks.RawHTMLBlock):

    def __init__(self,
                 required=True,
                 help_text=None,
                 max_length=None,
                 min_length=None,
                 validators=(),
                 **kwargs):

        super().__init__(**kwargs)
        self.field = forms.CharField(
            required=required,
            help_text=help_text,
            max_length=max_length,
            min_length=min_length,
            validators=validators,
            widget=CodeMirrorWidget)

    class Meta:
        label = 'HTML'
        icon = 'fa-code'
        group = _('Basic')


class ResponsiveImageBlock(blocks.StructBlock):
    padding = blocks.BooleanBlock(required=False)
    image = ImageChooserBlock()
    height = blocks.IntegerBlock(
        min_value=1,
        default=400,
    )
    link = blocks.URLBlock(required=False)

    class Meta:
        label = _('Responsive Image')
        icon = 'fa-picture-o'
        template = 'blocks/image.html'
        group = _('Basic')


class ParagraphBlock(blocks.StructBlock):
    alignment = blocks.ChoiceBlock([
        ("Left", _("Left")),
        ("Center", _("Center")),
        ("Right", _("Right"))
    ])
    text = blocks.RichTextBlock()

    class Meta:
        label = _('Paragraph')
        icon = 'edit'
        template = 'blocks/paragraph.html'
        group = _('Basic')


class HeadingBlock(blocks.StructBlock):
    title = CharBlock(required=True)
    title_alignment = ChoiceBlock(
        default=("Center", _("Center")),
        required=True,
        choices=[
            ("Left", _("Left")),
            ("Center", _("Center")),
            ("Right", _("Right"))],
        help_text=_("Choose the title alignment")
    )
    subtitle = CharBlock(required=False)
    subtitle_alignment = ChoiceBlock(
        default=("Center", _("Center")),
        required=True,
        choices=[
            ("Left", _("Left")),
            ("Center", _("Center")),
            ("Right", _("Right"))],
        help_text=_("Choose the subtitle alignment")
    )

    class Meta:
        label = _('Heading')
        icon = 'fa-header'
        template = 'blocks/title.html'
        group = _('Basic')


class DividerBlock(blocks.StaticBlock):

    class Meta:
        label = _('Divider')
        icon = 'horizontalrule'
        template = 'blocks/divider.html'
        group = _('Basic')


class ButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=True)
    link = blocks.URLBlock(required=True)

    class Meta:
        label = _('Button')
        icon = 'fa-hand-pointer-o'
        template = 'blocks/button.html'
        group = _('Basic')


class ButtonGroupBlock(blocks.StructBlock):
    buttons = blocks.ListBlock(ButtonBlock)

    class Meta:
        label = _('Buttons')
        icon = 'fa-hand-pointer-o'
        template = 'blocks/button_group.html'
        group = _('Basic')


class OverlayBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock(required=False)
    description = blocks.CharBlock(required=False)
    text_color = blocks.ChoiceBlock(choices=[
        ('text-light', _('Light')),
        ('text-dark', _('Dark')),
    ], default='text-dark')
    buttons = ButtonGroupBlock(required=False)

    class Meta:
        label = _('Image overlay')
        icon = 'fa-clone'
        template = 'blocks/overlay.html'
        group = _('Basic')


class IconBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    subtitle = blocks.CharBlock()
    icon = blocks.CharBlock(
        help_text=_('Material icon font icon text, as found on: '
                    'https://material.io/icons')
    )

    class Meta:
        label = _('Icon')
        icon = 'fa-file-excel-o'
        template = 'blocks/icon.html'
        group = _('Basic')


class IconGroupBlock(blocks.StructBlock):
    icons = blocks.ListBlock(IconBlock)

    class Meta:
        label = _('Icons')
        icon = 'fa-file-excel-o'
        template = 'blocks/icon_group.html'
        group = _('Basic')


class MemberCheckAPIBlock(blocks.StructBlock):

    class Meta:
        label = _('Member Check')
        icon = 'tick'
        template = 'blocks/member_check.html'
        group = _('Basic')


BASIC_BLOCKTYPES = [
    ('heading', HeadingBlock()),
    ('image', ResponsiveImageBlock()),
    ('image_overlay', OverlayBlock()),
    ('paragraph', ParagraphBlock()),
    ('divider', DividerBlock()),
    ('button_group', ButtonGroupBlock()),
    ('icons', IconGroupBlock()),
    ('instagram', InstagramFeedChooserBlock(
        help_text=_(
            "Instagram feeds are created in Branding in the left menu. "
            "If you can not see it, contact info@utn.se to get access"
        )
    )),
    ('member_check', MemberCheckAPIBlock()),
    ('html_code_block', HTMLCodeBlock()),
]


class CountdownBlock(blocks.StructBlock):

    size = blocks.ChoiceBlock(
        choices=[("S", _("Small")),
                 ("M", _("Medium")),
                 ("L", _("Large"))]
    )
    expires = blocks.DateTimeBlock()
    pre_title = blocks.CharBlock(required=False)

    # Allow the labels to contain whitespace so that the counter still
    # renders, but the label is empty. Leave label completely empty to
    # hide counter.
    years_label = blocks.CharBlock(
        required=False,
        help_text=_("leave empty to skip this counter in the countdown"),
    )
    years_label.field.strip = False
    months_label = blocks.CharBlock(
        required=False,
        help_text=_("leave empty to skip this counter in the countdown")
    )
    months_label.field.strip = False
    days_label = blocks.CharBlock(
        required=False,
        help_text=_("leave empty to skip this counter in the countdown")
    )
    days_label.field.strip = False
    hours_label = blocks.CharBlock(
        required=False,
        help_text=_("leave empty to skip this counter in the countdown")
    )
    hours_label.field.strip = False
    minutes_label = blocks.CharBlock(
        required=False,
        help_text=_("leave empty to skip this counter in the countdown")
    )
    minutes_label.field.strip = False
    seconds_label = blocks.CharBlock(
        required=False,
        help_text=_("leave empty to skip this counter in the countdown")
    )
    seconds_label.field.strip = False

    post_title = blocks.CharBlock(required=False)

    class Meta:
        label = _('Countdown')
        icon = 'fa-clock-o'
        template = 'blocks/countdown.html'
        group = _('Content')


# CONTENT BLOCKTYPES

class LogosBlock(blocks.StructBlock):
    logos = blocks.ListBlock(blocks.StructBlock([
        ('image', ImageChooserBlock()),
        ('link', blocks.URLBlock(required=False)),
        ('description', blocks.CharBlock(required=False))
    ]))

    class Meta:
        label = _('Logos')
        icon = 'fa-pied-piper'
        template = 'blocks/logos.html'
        group = _('Content')


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
        group = _('Content')


class EventsBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    show_facebook = blocks.BooleanBlock(
        required=False,
        help_text=_('Whether to embed a Facebook page')
    )
    facebook_page_name = blocks.CharBlock(
        required=False,
        help_text=_('Name of the page to show. (Must be public or accessible '
                    'by the registered app_id)')
    )

    show_youtube = blocks.BooleanBlock(
        required=False,
        help_text=_('Whether to show the last video from a Youtube-channel')
    )
    youtube_channel_id = blocks.CharBlock(
        required=False,
    )

    show_google_calendar = blocks.BooleanBlock(
        required=False,
        help_text=_('Whether to show the next few events from a '
                    'google calendar')
    )
    google_calendar_id = blocks.CharBlock(
        required=False,
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        left_count = 0
        for key in ['show_google_calendar', 'show_youtube']:
            if value[key]:
                left_count += 1

        right_count = 1 if value['show_facebook'] else 0

        two_cols = (left_count > 0 and right_count > 0)

        if two_cols:
            left_size = 8
        elif left_count > 0:
            left_size = 12
        else:
            left_size = 0

        right_size = 12 - left_size

        context['left_size'] = left_size
        context['right_size'] = right_size
        context['two_cols'] = two_cols

        return context

    class Meta:
        label = _('Events')
        icon = 'fa-calendar'
        group = _('Content')
        template = 'blocks/events.html'


class EventsBlockAdapter(StructBlockAdapter):
    """Javascript adaptor for the events block in the editing view"""

    js_constructor = 'moore.blocks.EventsBlock'

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ['js/events_block.js'],
            css=structblock_media._css
        )


register(EventsBlockAdapter(), EventsBlock)


class ContactsBlock(blocks.StructBlock):
    contacts = blocks.ListBlock(ContactCardBlock())

    class Meta:
        label = _('Contact Card')
        icon = 'user'
        template = 'involvement/blocks/contact_cards.html'
        group = _('Content')


class EventbriteBlock(blocks.StructBlock):
    eventbriteToken = blocks.CharBlock(required=True)

    def getEventsJson(self, token):
        headers = {"Authorization": 'Bearer ' + token}
        r = requests.get(
            'https://www.eventbriteapi.com/v3/users/me/events/' +
            '?status=live&time_filter=current_future&expand=venue',
            headers=headers
        )
        return r.json()

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        try:
            eventsJson = self.getEventsJson(value['eventbriteToken'])
            for evt in eventsJson['events']:
                evt['starttime'] = datetime.strptime(
                    evt['start']['local'],
                    '%Y-%m-%dT%H:%M:%S'
                )
                evt['endtime'] = datetime.strptime(
                    evt['end']['local'],
                    '%Y-%m-%dT%H:%M:%S'
                )
                context['events'] = eventsJson['events']
        except Exception:
            context['error'] = 'Failed to retrieve events from eventbrite.'
        finally:
            return context

    class Meta:
        label = _('Eventbrite')
        icon = 'fa-pied-piper'
        template = 'blocks/eventbrite.html'
        group = _('Content')


class ImageTextCardBlock(blocks.StructBlock):
    cards = blocks.ListBlock(blocks.StructBlock([
        ('image', ImageChooserBlock()),
        ('title', blocks.CharBlock()),
        ('text', blocks.RichTextBlock(required=False))
    ]))

    class Meta:
        label = _('Image + Text Cards')
        icon = 'fa-picture-o'
        template = 'blocks/image_text_cards.html'
        group = _('Content')


CONTENT_BLOCKTYPES = [
    ('countdown', CountdownBlock()),
    ('contacts', ContactsBlock()),
    ('events', EventsBlock()),
    ('logos', LogosBlock()),
    ('counters', CountersBlock()),
    ('image_text_card', ImageTextCardBlock()),
]

# INLINE LAYOUT BLOCKTYPES


class AccordionBlock(blocks.StructBlock):
    rows = blocks.ListBlock(blocks.StructBlock([
        ('header',  blocks.CharBlock()),
        ('body', blocks.StreamBlock(BASIC_BLOCKTYPES))
    ]))

    class Meta:
        label = _('Accordion')
        icon = 'fa-bars'
        template = 'blocks/accordion.html'
        group = _('Layout')


class ModalImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    body = blocks.StreamBlock(BASIC_BLOCKTYPES)

    class Meta:
        label = _('Modal Image')
        icon = 'fa-ghost'
        template = 'blocks/modal.html'
        group = _('Layout')


INLINE_LAYOUT_BLOCKTYPES = BASIC_BLOCKTYPES + [
    ("Accordion", AccordionBlock()),
    ('modal_image', ModalImageBlock()),
]


# LAYOUT BLOCKTYPES

class ColumnBlock(blocks.StructBlock):
    columns = blocks.ListBlock(blocks.StructBlock([
        ('width', blocks.ChoiceBlock(
            [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
             (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)],
            help_text=_('Width out of 12'),
        )),
        ('content', blocks.StreamBlock(INLINE_LAYOUT_BLOCKTYPES))
    ]))

    class Meta:
        label = _('Columns')
        icon = 'fa-columns'
        template = 'blocks/columns.html'
        group = _('Layout')


class TwoColumnGridBlock(blocks.StructBlock):
    height = blocks.IntegerBlock(
        min_value=1,
        default=400,
        max_value=800,
        help_text=_('Row height in px')
    )
    rows = blocks.ListBlock(blocks.StructBlock([
        ('flip', blocks.BooleanBlock(
            required=False,
            help_text=_('Swap position of image and paragraph'),
        )),
        ('image', ImageChooserBlock()),
        ('paragraph', ParagraphBlock()),
    ]))

    class Meta:
        label = _('Two Column Grid')
        icon = 'fa-columns'
        template = 'blocks/two_column_grid.html'
        group = _('Layout')


LAYOUT_BLOCKTYPES = [
    ('columns', ColumnBlock()),
    ('two_column_grid', TwoColumnGridBlock()),
]


SECTION_CONTENT_BLOCKTYPES = INLINE_LAYOUT_BLOCKTYPES + \
                             LAYOUT_BLOCKTYPES + \
                             CONTENT_BLOCKTYPES


class SectionBlock(blocks.StructBlock):
    padding = blocks.ChoiceBlock(
        required=False,
        choices=[("S", _("Small")), ("M", _("Medium")), ("L", _("Large"))],
        help_text=_("Include padding for this section")
    )
    full_width = blocks.BooleanBlock(
        required=False,
        help_text=_("Expand this section to full page width")
    )

    body = blocks.StreamBlock(SECTION_CONTENT_BLOCKTYPES)

    class Meta:
        label = _('Section')
        icon = 'fa-bars'
        template = 'blocks/section.html'
        group = _('Sections')


PAGE_BLOCKTYPES = [
    ('section', SectionBlock()),
    ('divider', DividerBlock()),
]

WAGTAIL_STATIC_BLOCKTYPES = PAGE_BLOCKTYPES
