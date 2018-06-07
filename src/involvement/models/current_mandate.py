from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.models import ClusterableModel


class CurrentMandate(ClusterableModel):
    position = models.ForeignKey(
        'Position',
        related_name='current_mandate',
        on_delete=models.PROTECT,
        blank=False,
    )

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=False,
    )

    class Meta:
        verbose_name = _('Current mandate')
        verbose_name_plural = _('Current mandates')
        unique_together = ('position', 'applicant')
        default_permissions = ()
