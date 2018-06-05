from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, \
    InlinePanel, FieldRowPanel


class Application(ClusterableModel):
    """An application is made to strive to acquire an position"""

    position = models.ForeignKey(
        'Position',
        related_name='applications',
        on_delete=models.PROTECT,
        blank=False,
    )

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=False,
    )

    class Meta:
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')
        unique_together = ('position', 'applicant')
        default_permissions = ()

    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('submitted', _('Submitted')),
        ('approved', _('Approved')),
        ('disapproved', _('Disapproved')),
        ('appointed', _('Appointed')),
        ('turned_down', _('Turned down')),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name=_('Status'),
        blank=False,
        null=False,
    )

    # ---- Application Information ------
    cover_letter = models.TextField(
        verbose_name=_('Cover Letter'),
        help_text=_('Present yourself and state why you are who we are '
                    'looking for'),
        blank=True,
    )
    qualifications = models.TextField(
        verbose_name=_('Qualifications'),
        help_text=_('Give a summary of relevant qualifications'),
        blank=True,
    )

    # Access overhead
    removed = models.BooleanField(
        default=False,
    )

    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('applicant'),
            FieldPanel('position'),
        ]),
        FieldPanel('cover_letter'),
        FieldPanel('qualifications'),
        InlinePanel('references'),
        FieldPanel('status'),
    ])]
