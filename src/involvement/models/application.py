from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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

    def __str__(self) -> str:
        return '%(applicant)s - %(position)s' % {
            'position': self.position,
            'applicant': self.applicant
        }

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


@receiver(post_save, sender=Application,
          dispatch_uid='application_check_mandate_history')
def check_mandate_history(sender, instance, **kwargs):
    MandateHistory = apps.get_model('involvement', 'MandateHistory')
    if instance.status == 'appointed':
        MandateHistory.objects.get_or_create(
            position=instance.position,
            applicant=instance.applicant,
        )
    else:
        MandateHistory.objects.filter(
            position=instance.position,
            applicant=instance.applicant,
        ).delete()


@receiver(post_save, sender=Application,
          dispatch_uid='application_check_contact_card')
def check_contact_card(sender, instance, **kwargs):
    ContactCard = apps.get_model('involvement', 'ContactCard')

    if instance.status == 'appointed':
        if not hasattr(instance, 'contact_card'):
            # Take a vacant position if available or create a new
            card = ContactCard.objects.filter(
                position=instance.position,
                application__isnull=True,
            ).first()

            if card:
                card.application = instance
                card.picture = None
                card.save()
            else:
                ContactCard.objects.create(
                    position=instance.position,
                    application=instance,
                )

    else:
        if hasattr(instance, 'contact_card'):
            # Remove card if appointments for the position is not enough.
            # Otherwise set card as vacant
            card = instance.contact_card
            cards_count = instance.position.contact_cards.count()
            if instance.position.appointments < cards_count:
                card.delete()
            else:
                card.application = None
                card.picture = None
                card.save()
