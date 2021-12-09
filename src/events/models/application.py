from django.db import models
from django.apps import apps
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, \
    InlinePanel, FieldRowPanel

class EventApplication(models.Model):
    """A ticket type determines what allows a user entry to an event"""

    event_applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
    )

    event = models.ForeignKey(
        'Event',
        on_delete=models.PROTECT,
        blank=False,
    )

    class Meta:
        verbose_name = _('Event Application')
        verbose_name_plural = _('Event Applications')
        default_permissions = ()

    # Access overhead
    removed = models.BooleanField(
        default=False,
    )

    # ------ Administrator settings ------
    panels = [
        FieldPanel('event_applicant'),
        FieldPanel('event'),
    ]

    def __str__(self):
        return "Application by " + str(self.event_applicant) + " " + str(self.event_applicant.person_nr)
