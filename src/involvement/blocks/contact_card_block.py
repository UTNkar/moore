from django.utils.translation import gettext_lazy as _
from wagtail.snippets.blocks import SnippetChooserBlock


class ContactCardBlock(SnippetChooserBlock):
    def __init__(self, **kwargs):
        super(ContactCardBlock, self).__init__(
            'involvement.ContactCard', **kwargs
        )

    class Meta:
        label = _('Contact Card')
        icon = 'user'
        template = 'involvement/blocks/contact_card.html'
        group = _('Meta')
