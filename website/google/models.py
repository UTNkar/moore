from wagtail.wagtailcore import blocks

from django.utils.translation import ugettext_lazy as _


class GoogleFormBlock(blocks.StructBlock):
    form_id = blocks.CharBlock()
    height = blocks.IntegerBlock()

    class Meta:
        label = _('Google Form')
        icon = 'fa-check-square-o'
        template = 'google/blocks/form.html'


class GoogleDriveBlock(blocks.StructBlock):
    folder_id = blocks.CharBlock()
    view = blocks.ChoiceBlock(choices=[
        ('list', _('List')),
        ('grid', _('Grid')),
    ])
    height = blocks.IntegerBlock()

    class Meta:
        label = _('Google Drive')
        icon = 'fa-folder-open'
        template = 'google/blocks/drive.html'
