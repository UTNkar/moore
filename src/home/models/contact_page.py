from __future__ import absolute_import, unicode_literals
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page
from utils.translation import TranslatedField
from involvement.blocks import ContactCardBlock


class ContactPage(Page):
    # ---- General Page information ------
    title_sv = models.CharField(max_length=255)
    translated_title = TranslatedField('title', 'title_sv')

    contact_point = StreamField(
        [('person', ContactCardBlock())],
    )

    other_contacts = StreamField(
        [('contact', blocks.StructBlock([
            ('person', ContactCardBlock()),
            ('english_groups', blocks.CharBlock(
                help_text=_('Comma separated list of English group names.'),
                required=False,
            )),
            ('swedish_groups', blocks.CharBlock(
                help_text=_('Comma separated list of Swedish group names.'),
                required=False,
            )),
        ], icon='user'))],
    )

    map_location = models.CharField(
        max_length=255,
        verbose_name=_('Map Location'),
        help_text=_('Enter comma separated coordinates'),
        blank=True,
    )

    location_description = RichTextField(
        verbose_name=_('Location Description'),
        help_text=_('Enter the text to show on the map'),
        blank=True,
    )

    def get_context(self, request, *args, **kwargs):
        contacts = {}
        for contact in self.other_contacts:
            if request.LANGUAGE_CODE == 'sv':
                groups = contact.value.get('swedish_groups', '')
            else:
                groups = contact.value.get('english_groups', '')
            groups = groups.split(',')

            for group in groups:
                group = group.strip()
                list = contacts.get(group, [])
                list.append(contact.value['person'])
                contacts[group] = list

        context = super(ContactPage, self).get_context(
            request, *args, **kwargs
        )
        context['contacts'] = contacts
        return context

    content_panels = Page.content_panels + [
        FieldPanel('title_sv', classname="full title"),
        FieldPanel('map_location'),
        FieldPanel('location_description'),
        StreamFieldPanel('contact_point'),
        StreamFieldPanel('other_contacts'),
    ]
