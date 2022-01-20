from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel


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
