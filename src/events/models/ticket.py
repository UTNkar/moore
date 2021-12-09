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
        on_delete=models.PROTECT,
        blank=False,
    )

    ticket_number = models.IntegerField(
        verbose_name=_('Ticket number'),
    )

    num_extra_participants = models.IntegerField(
        verbose_name=_('Extra participants'),
        help_text=_('Dictates the number of participants in the ticket besides the ticket owner.'),
        default=0)

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        default_permissions = ()
        # constraints = [
        #     UniqueConstraint(fields=['event, ticket_number'], name='pk-constraint'),
        # ]

    STATUS_CHOICES = (
        ('unassigned', _('Unassigned')),
        ('assigned', _('Assigned')),
    )

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
    ]
