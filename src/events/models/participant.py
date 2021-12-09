from django.db import models
from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, \
    InlinePanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from members.fields import PersonNumberField

class Participant(models.Model):
    name = models.CharField(
        help_text=_('This field identifies the participant type.'),
        verbose_name=_('Participant name'),
        max_length=255
    )

    person_nr = models.CharField(
        verbose_name=_('Person number'),
        help_text=_('Person number using the YYYYMMDD-XXXX format.'),
        max_length=13
    )

    # The order is the result of submitting the form, but that form
    # depends on what price list is associated with the event.
    order = models.JSONField(default=dict)

    panels = [MultiFieldPanel([
        FieldPanel('name'),
        FieldPanel('person_nr'),
    ])]

    costs = models.ForeignKey('Costs',
                              on_delete=models.SET_NULL,
                              null=True)

    ticket = models.ForeignKey('Ticket',
                               on_delete=models.CASCADE)


    class Meta:
        verbose_name = _('ParticipantType')
        verbose_name_plural = _('ParticipantTypes')
        default_permissions = ()
        ordering = ['name']

    def __str__(self):
        return str(self.name) + str(self.person_nr) + str(self.order)
