from __future__ import absolute_import, unicode_literals
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.fields import StreamField, RichTextField
from wagtail.models import Page
from utils.translation import TranslatedField
from involvement.blocks import ContactCardBlock


class ContactPage(Page):
    # ---- General Page information ------
    title_sv = models.CharField(max_length=255)
    translated_title = TranslatedField('title', 'title_sv')

    contact_point = StreamField(
        [('person', ContactCardBlock())],
        use_json_field=True,
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
        use_json_field=True,
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
        FieldPanel('contact_point'),
        FieldPanel('other_contacts'),
    ]
