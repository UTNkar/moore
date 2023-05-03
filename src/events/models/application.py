from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from django.db.models.signals import post_save
from events.models import Ticket


class EventApplication(models.Model):
    event_applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
    )

    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        blank=False,
    )

    ticket = models.ForeignKey(
        'Ticket',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Event Application')
        verbose_name_plural = _('Event Applications')

    # Access overhead
    removed = models.BooleanField(
        default=False,
    )

    # ------ Administrator settings ------
    panels = [
        FieldPanel('event_applicant'),
        FieldPanel('event'),
        FieldPanel('ticket'),
    ]

    def __str__(self):
        return ("Application by "
                + str(self.event_applicant)
                + " "
                + str(self.event_applicant.person_nr))


@receiver(post_save, sender=EventApplication)
def ensure_ticket(sender, instance, created, **kwargs):
    # Ensure that if someone who already holds a ticket makes an application
    # their ticket is correctly registered with the application.
    # This fixes a bug where someone could get a ticket but their
    # application was ticketless, and so participate in future raffles.
    ticket = Ticket.objects.filter(
        event=instance.event,
        owner=instance.event_applicant
    )
    if ticket.exists() and instance.ticket is None:
        instance.ticket = ticket[0]
        instance.save()
