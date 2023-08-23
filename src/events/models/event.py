from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, \
    FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.snippets.models import register_snippet
from events.models import Ticket


@register_snippet
class Event(models.Model):
    title = models.CharField(
        help_text='This is the display name for the event',
        verbose_name='Name of event',
        max_length=255
    )

    description = RichTextField(
        help_text=_(
            'This is the long text shown as description for the event.'),
        verbose_name=_('Description for event'),
        max_length=1000
    )

    info_for_participants = RichTextField(
        help_text=_(
            'This separate information will be '
            'presented to those who recieve tickets.'),
        verbose_name=_('Information for participants'),
        null=True,
        blank=True,
        max_length=1000,
    )

    start_date = models.DateTimeField(
        verbose_name=_('Event start time'),
        help_text=_('This dictates when the event is considered as ongoing.')
    )

    end_date = models.DateTimeField(
        verbose_name=_('Event end time'),
        help_text=_('This dictates when the event is considered finished.')
    )

    end_of_application = models.DateTimeField(
        verbose_name=_('Application end time'),
        help_text=_('After this date it will no longer be possible to apply.'),
    )

    num_tickets = models.IntegerField(
        verbose_name=_('Number of entries'),
        help_text=_('This dictates the number of individual entries to the '
                    'event.'),
        default=1
    )

    num_participants_per_ticket = models.IntegerField(
        verbose_name=_('Number of participants per ticket'),
        help_text=_('This dictates the number of participants per ticket. '
                    'For example, the ball would set this to 2. '
                    'Don\'t set this to be less than 1.'),
        default=1
    )

    base_price = models.IntegerField(
        help_text=_('Base ticket price. For example, 600 for a rally entry.'),
        verbose_name=_('Ticket price'),
        default=0
    )

    base_price_nonmember = models.IntegerField(
        help_text=_('Base ticket price for non-members.'),
        verbose_name=_('Ticket price for non-members'),
        default=0
    )

    price_per_participant = models.IntegerField(
        help_text=_(
            'Price per participant, independent of their order. '
            'For example, 1100 for a ball seat'),
        verbose_name=_('Price per participant'),
        default=0
    )

    price_per_participant_nonmember = models.IntegerField(
        help_text=_(
            'Price per non-UTN-member participant, excluding of their order. '
            'For example, 1200 for a ball seat'),
        verbose_name=_('Price per non-member participant'),
        default=0
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
        help_text=_(
            'Immediately assign applicants first-come-first-serve. '
            'Not suitable for events that raffle their entries.')
    )

    last_payment_date = models.DateTimeField(
        verbose_name=_('Event final payment date & time'),
        help_text=_(
            'After this time, the event is no longer payed for'
            ', and unpaid tickets are invalidated.'),
        null=True
    )

    published = models.BooleanField(
        default=False,
        verbose_name=_('Event published'),
        help_text=_('Determines if the event is visible or not')
    )

    contact_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_('Email for contact'),
        help_text=_('Email address for who to contact regarding this event.')
    )

    raffle_has_been_held = models.BooleanField(
        default=False,
        verbose_name=_('Raffle has been held'),
        help_text=_('This signals to users whether a raffle has been held. '
                    'This field populates automatically once a '
                    ' raffle has been held.')
    )

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ['title']

    # Access overhead
    removed = models.BooleanField(
        default=False,
    )

    def __str__(self) -> str:
        return self.title
    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
        FieldPanel('title'),
        ImageChooserPanel('image'),
        FieldPanel('description'),
        FieldPanel('info_for_participants'),
        FieldPanel('end_of_application'),
        FieldRowPanel([
            FieldPanel('num_tickets'),
            FieldPanel('num_participants_per_ticket'),
        ]),
        FieldPanel('first_come_first_serve'),
        FieldRowPanel([
            FieldPanel('base_price'),
            FieldPanel('base_price_nonmember'),
        ]),
        FieldRowPanel([
            FieldPanel('price_per_participant'),
            FieldPanel('price_per_participant_nonmember'),
        ]),
        FieldPanel('price_list'),
        FieldPanel('last_payment_date'),
        FieldRowPanel([
            FieldPanel('start_date'),
            FieldPanel('end_date'),
        ]),
        FieldPanel('contact_email'),
        FieldPanel('published'),
        FieldPanel('raffle_has_been_held'),
    ])
    ]

    def is_free(self):
        price_list_cost = sum([order['Price']
                              for order in self.price_list.fields])
        cost = self.base_price + self.price_per_participant + price_list_cost
        return cost == 0


@receiver(post_save, sender=Event)
def post_save(sender, instance, created, **kwargs):
    if created:
        event = instance
        tickets = []

        for ticket_number in range(1, event.num_tickets + 1):
            if Ticket.objects.filter(ticket_number=ticket_number,
                                     event=event).count() == 0:
                tickets.append(
                    Ticket(
                        ticket_number=ticket_number,
                        event=event,
                        owner=None
                    )
                )

        Ticket.objects.bulk_create(tickets)
