from datetime import date
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, \
    FieldRowPanel
from utils.translation import TranslatedField


class Position(models.Model):
    """Position represents the execution of a role within UTN"""

    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')
        default_permissions = ()

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
