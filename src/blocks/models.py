from django.utils.translation import ugettext_lazy as _
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from involvement.blocks import ContactCardBlock
import requests
from datetime import datetime


class ResponsiveImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    height = blocks.IntegerBlock(
        min_value=1,
        default=400,
    )

    class Meta:
        label = _('Responsive Image')
        icon = 'fa-picture-o'
        template = 'blocks/image.html'
        group = _('Basic')


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
        group = _('Noyce')


class OverlayBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    title = blocks.CharBlock(required=False)
    description = blocks.CharBlock(required=False)
    text_color = blocks.ChoiceBlock(choices=[
        ('text-light', _('Light')),
        ('text-dark', _('Dark')),
    ], default='text-dark')
    link = blocks.URLBlock(required=False)
    button = blocks.CharBlock(required=False)

    class Meta:
        label = _('Image overlay')
        icon = 'fa-clone'
        template = 'blocks/overlay.html'
        group = _('Noyce')


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

    show_instagram = blocks.BooleanBlock(
        required=False,
        help_text=_('Whether to show Instagram the last event from the '
                    'registered Instagram feed')
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
        for key in ['show_google_calendar', 'show_instagram', 'show_youtube']:
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

        if two_cols:
            insta_cal_size = 6 if value['show_google_calendar'] \
                and value['show_instagram'] \
                else 12
        else:
            insta_cal_size = 4

        context['left_size'] = left_size
        context['right_size'] = right_size
        context['insta_cal_size'] = insta_cal_size
        context['two_cols'] = two_cols

        return context

    class Meta:
        label = _('Events')
        icon = 'fa-calendar'
        group = _('Noyce')
        form_template = 'block_forms/events.html'
        template = 'blocks/events.html'


class ContactsBlock(blocks.StructBlock):
    contacts = blocks.ListBlock(ContactCardBlock())

    class Meta:
        label = _('Contact Card')
        icon = 'user'
        template = 'involvement/blocks/contact_cards.html'
        group = _('Meta')


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
        group = _('Embed')


BASIC_BLOCKTYPES = [
    ('paragraph', blocks.RichTextBlock(
        template='blocks/paragraph.html',
        group=_('Basic'),
    )),
    ('image', ResponsiveImageBlock()),
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
        ('paragraph', blocks.RichTextBlock(
            template='blocks/paragraph.html',
            group=_('Basic'),
        ))
    ]))

    class Meta:
        label = _('Two Column Grid')
        icon = 'fa-columns'
        template = 'blocks/two_column_grid.html'
        group = _('Noyce')


WAGTAIL_STATIC_BLOCKTYPES = BASIC_BLOCKTYPES + [
    ('heading', HeadingBlock()),  # TODO: Do we use this one?
    ('image_description', ImageIconsBlock()),
    ('image_icons', ImageDescriptionBlock()),
    ('overlay', OverlayBlock()),
    ('logos', LogosBlock()),
    ('counters', CountersBlock()),
    ('columns', ColumnBlock()),
    ('contacts', ContactsBlock()),
    ('events', EventsBlock()),
    ('two_column_grid', TwoColumnGridBlock())
]
