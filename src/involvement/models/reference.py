from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, \
    FieldRowPanel
from wagtail.core.models import Orderable


class Reference(Orderable):
    """Reference represents a reference given in an application"""

    application = ParentalKey(
        'Application',
        related_name='references',
        on_delete=models.CASCADE,
        blank=False,
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        help_text=_('Enter the name of your reference'),
        blank=False,
    )

    position = models.CharField(
        max_length=255,
        verbose_name=_('Position'),
        help_text=_('Enter the position in which your reference relates to '
                    'you'),
        blank=False,
    )

    email = models.EmailField(
        verbose_name=_('email address'),
        help_text=_('Enter an email address on which your reference in '
                    'reachable'),
        blank=True,
    )

    phone_number = models.CharField(
        max_length=20,
        verbose_name=_('Phone number'),
        help_text=_('Enter a valid phone number'),
        validators=[validators.RegexValidator(
            regex=r'^\+?\d+$',
            message=_('Enter a phone number on which your reference is '
                      'reachable'),
        )],
        blank=True,
    )

    comment = models.CharField(
        max_length=500,
        verbose_name=_('Comment'),
        help_text=_('Enter any additional comments regarding your reference'),
        blank=True,
    )

    def __str__(self) -> str:
        ref = '%s - %s' % (self.name, self.position)
        if self.phone_number and self.email:
            ref += '\nContact: %s or %s' % (self.phone_number, self.email)
        elif self.phone_number or self.email:
            ref += '\nContact: %s' % self.phone_number + self.email
        if self.comment:
            ref += '\nComment: %s' % self.comment

        return ref

    # ------ Administrator settings ------
    panels = [MultiFieldPanel([
        FieldRowPanel([
            FieldPanel('name'),
            FieldPanel('position'),
        ]),
        FieldRowPanel([
            FieldPanel('email'),
            FieldPanel('phone_number'),
        ]),
        FieldPanel('comment'),
    ])]
