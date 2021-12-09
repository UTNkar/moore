from django.utils.translation import gettext_lazy as _
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.core import blocks

class EventBlock(SnippetChooserBlock):
    def __init__(self, **kwargs):
        super(EventBlock, self).__init__(
            'events.Event', **kwargs
        )

    class Meta:
        label = _('Event')
        icon = 'fa-ticket'
        template = 'events/blocks/event.html'
        group = _('Content')

class EventListBlock(blocks.StructBlock):
    events = blocks.ListBlock(EventBlock)

    class Meta:
        label = _('Event list')
        icon = 'fa-ticket'
        template = 'events/blocks/event_list.html'
        grou = _('Content')
