from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.models import ClusterableModel


class MandateHistory(ClusterableModel):
    position = models.ForeignKey(
        'Position',
        related_name='mandate_histories',
        on_delete=models.PROTECT,
        blank=False,
    )

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=False,
    )

    class Meta:
        verbose_name = _('Mandate history')
        verbose_name_plural = _('Mandate histories')
        unique_together = ('position', 'applicant')
        default_permissions = ()
