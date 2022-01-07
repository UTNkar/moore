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
import events.models as event_models

class Ticket(models.Model):
    """A ticket type determines what allows a user entry to an event"""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        blank=False,
    )

    ticket_number = models.IntegerField(
        verbose_name=_('Ticket number'),
    )

    num_extra_participants = models.IntegerField(
        verbose_name=_('Extra participants'),
        help_text=_('Dictates the number of participants in the ticket besides the ticket owner.'),
        default=0)

    locked = models.BooleanField(
        default=False,
        verbose_name=_("Locked for payment"),
        help_text=_("This field is filled in if the ticket owner has signaled that they are ready to pay."))

    PAYMENT_STATUSES = (
        ('unpaid', ('Unpaid')),
        ('pending', ('Payment pending')),
        ('paid', ('Paid')),
    )

    payment_status = models.CharField(
        max_length = 16,
        choices=PAYMENT_STATUSES,
        blank=False,
        null=False,
        default='unpaid',
    )

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        default_permissions = ()

    # Access overhead
    removed = models.BooleanField(
        default=False,
    )

    def num_participants(self):
        return self.event.num_participants_per_ticket

    def __str__(self) -> str:
        return 'Ticket %s for event "%s"' % (
            str(self.ticket_number),
            str(self.event),
)

    # ------ Administrator settings ------
    panels = [
        FieldPanel('owner'),
        FieldPanel('event'),
        FieldPanel('ticket_number'),
        FieldPanel('locked'),
    ]

@receiver(post_save, sender=Ticket)
def post_save(sender, instance, created, **kwargs):
    if not created:
        ticket = instance
        participants = event_models.Participant.objects.filter(ticket=ticket).order_by('id')

        if ticket.owner is not None:
            if participants.count() < 1:
                event_models.Participant(name=ticket.owner.name, person_nr=ticket.owner.person_nr, ticket=ticket).save()
            else:
                owner = participants[0]
                owner.person_nr = ticket.owner.person_nr
                owner.save()
