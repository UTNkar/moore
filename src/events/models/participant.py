from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel
from utils.melos_client import MelosClient


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

    ticket = models.ForeignKey('Ticket',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('ParticipantType')
        verbose_name_plural = _('ParticipantTypes')
        default_permissions = ()
        ordering = ['name']

    def __str__(self):
        return str(self.name) + str(self.person_nr) + str(self.order)

    def calculate_order_cost(self):
        cost = 0
        price_list = self.ticket.event.price_list
        is_member = self.person_nr and MelosClient.is_member(self.person_nr)

        if is_member:
            cost += self.ticket.event.price_per_participant
        else:
            cost += self.ticket.event.price_per_participant_nonmember

        for orderable in price_list.fields:
            if self.order.get(orderable['Name']):
                if is_member:
                    cost += orderable.get('Price', 0)
                else:
                    cost += orderable.get('Non-member price', 0)

        return cost
