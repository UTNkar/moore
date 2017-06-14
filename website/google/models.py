from wagtail.wagtailcore import blocks

from django.utils.translation import ugettext_lazy as _


class GoogleFormBlock(blocks.StructBlock):
    form_id = blocks.CharBlock()
    height = blocks.IntegerBlock()

    class Meta:
        label = _('Google Form')
        icon = 'fa-check-square-o'
        template = 'google/blocks/form.html'
