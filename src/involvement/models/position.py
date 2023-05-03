from datetime import date
from django.apps import apps
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import MultiFieldPanel, FieldPanel, \
    FieldRowPanel
from utils.translation import TranslatedField


class Position(models.Model):
    """Position represents the execution of a role within UTN"""

    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')
        default_permissions = ()
        ordering = ['role']

    role = models.ForeignKey(
        'Role',
        related_name='positions',
        on_delete=models.PROTECT,
        blank=False,
    )

    recruitment_start = models.DateField(
        verbose_name=_('Start of recruitment'),
        default=date.today,
    )
    recruitment_end = models.DateField(verbose_name=_('Recruitment deadline'))

    # ---- Appointment Information ------
    appointments = models.IntegerField(
        verbose_name=_('Number of appointments'),
        help_text=_('Enter the number of concurrent appointments to the '
                    'position'),
        default=1,
    )

    term_from = models.DateField(verbose_name=_('Date of appointment'))

    term_to = models.DateField(verbose_name=_('End date of appointment'))

    comment_en = models.TextField(
        verbose_name=_('English extra comments'),
        help_text=_('Enter extra comments specific to the position this '
                    'year.'),
        blank=True,
    )

    comment_sv = models.TextField(
        verbose_name=_('Swedish extra comments'),
        help_text=_('Enter extra comments specific to the position this '
                    'year.'),
        blank=True,
    )

    comment = TranslatedField('comment_en', 'comment_sv')

    def __str__(self) -> str:
        if self.term_from.year != self.term_to.year:
            return "%s %s-%s" \
                   % (self.role.name, self.term_from.year, self.term_to.year)
        else:
            return "%s %s" % (self.role.name, self.term_from.year)

    @property
    def long_name(self):
        """
        Return the long name of this position.

        The long name contains the team_names that the positions role
        is a part of
        """
        return '%(position)s %(separator)s %(teams)s' % {
                'position': str(self),
                'separator': _('in'),
                'teams': self.role.team_names
            }
    # fget is a python thing that is needed since long_name is a property
    long_name.fget.short_description = _('Position')
    long_name.fget.admin_order_field = 'position'

    @property
    def appointed_applications(self):
        Application = apps.get_model('involvement', 'Application')
        return Application.objects.filter(
            status='appointed',
            position=self,
        )

    @property
    def is_past_due(self):
        return date.today() > self.recruitment_end

    def current_action(self) -> str:
        if self.is_past_due:
            applications = self.applications.exclude(status='draft')
            if applications.all().filter(status='submitted').exists():
                return 'approve'
            elif applications.all().filter(status='appointed') \
                    .count() >= self.appointments:
                return 'done'
            else:
                return 'appoint'
        else:
            return 'recruit'

    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('role'),
            FieldPanel('appointments'),
        ]),
        FieldRowPanel([
            FieldPanel('term_from'),
            FieldPanel('term_to'),
        ]),
        FieldRowPanel([
            FieldPanel('recruitment_start'),
            FieldPanel('recruitment_end'),
        ]),
        FieldPanel('comment_en'),
        FieldPanel('comment_sv'),
    ])]


@receiver(post_save, sender=Position,
          dispatch_uid='position_check_contact_card')
def position_check_contact_card(sender, instance, **kwargs):
    ContactCard = apps.get_model('involvement', 'ContactCard')
    cards = ContactCard.objects.filter(
        position=instance,
    )
    if cards.count() < instance.appointments:
        # We should create vacant contact cards
        for i in range(0, instance.appointments - cards.count()):
            ContactCard.objects.create(position=instance)

    if cards.count() > instance.appointments:
        # We have more cards that should be available.
        # Remove only vacant contact cards.
        maxCardsToRemove = cards.count() - instance.appointments
        removedCards = 0
        for card in cards.filter(application__isnull=True).all():
            card.delete()
            removedCards += 1
            if removedCards == maxCardsToRemove:
                break


@receiver(post_save, sender=Position,
          dispatch_uid='position_sync_user_groups')
def sync_user_groups(sender, instance, **kwargs):
    for appl in instance.appointed_applications.all():
        appl.applicant.sync_user_groups()
