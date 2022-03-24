from django.utils.translation import gettext_lazy as _
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.core import blocks
from events.models import Ticket


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

    def get_context(self, value, parent_context=None):
        ctx = super().get_context(value, parent_context=parent_context)

        for event in ctx['self']['events']:
            event.user_has_ticket = Ticket.objects.filter(
                owner=ctx['user'], event=event
            ).exists()

        return ctx

    class Meta:
        label = _('Event list')
        icon = 'fa-ticket'
        template = 'events/blocks/event_list.html'
        grou = _('Content')
