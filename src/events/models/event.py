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
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

@register_snippet
class Event(models.Model):
    title = models.CharField(
        help_text='This is the display name for the event',
        verbose_name='Name of event',
        max_length=255
    )

    description = models.TextField(
        help_text=_('This is the long text shown as description for the event.'),
        verbose_name=_('Description for event'),
        max_length=1000
    )

    start_date = models.DateTimeField(
        verbose_name=_('Event start time'),
        help_text=_('This dictates when the event is considered as ongoing.')
    )

    end_date = models.DateTimeField(
        verbose_name=_('Event end time'),
        help_text=_('This dictates when the event is considered finished.')
    )

    num_tickets = models.IntegerField(
        verbose_name=_('Number of entries'),
        help_text=_('This dictates the number of individual entries to the '
                    'event.'),
        default=1
    )

    num_participants_per_ticket = models.IntegerField(
        verbose_name=_('Number of participants per ticket'),
        help_text=_('This dictates the number of participants that each ticket entry allows. '
                    'For example, the puzzle hunt rally would want this to be 9. '
                    'Don\'t set this to be less than 1.'),
        default=1
    )

    price_list = models.ForeignKey(
        'Costs',
        verbose_name=_('Price list'),
        help_text=_('The price list for each participant'),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name=_('Image'),
        help_text=_('Recommended size of TODO'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    first_come_first_serve = models.BooleanField(
        default=False,
        verbose_name=_('First come first serve'),
        help_text=_('Immediately assign applicants first-come-first-serve. Not suitable for events that raffle their entries.')
    )


    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        default_permissions = ()
        ordering = ['title']

    STATUS_CHOICES = (
        ('published', _('Published')),
        ('unpublished', _('Unpublished')),
        ('ongoing', _('Ongoing')),
        ('finished', _('Finished')),
    )

    # Access overhead
    removed = models.BooleanField(
        default=False,
    )

    def __str__(self) -> str:
        return self.title
    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('num_tickets'),
        FieldPanel('num_participants_per_ticket'),
        FieldPanel('price_list'),
        FieldRowPanel([
            FieldPanel('start_date'),
            FieldPanel('end_date'),
            ]),
        ImageChooserPanel('image'),
        ])
    ]
