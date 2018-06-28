from datetime import date
from django.apps import apps
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


class ContactBlockForm(WagtailAdminModelForm):

    def __init__(self, *args, **kwargs):
        super(ContactBlockForm, self).__init__(*args, **kwargs)
        contact_card = self.instance
        Application = apps.get_model('involvement', 'Application')

        if contact_card.application:
            self.fields['application'].queryset = Application.objects.filter(
                models.Q(
                    position__term_from__lte=date.today(),
                    position__term_to__gte=date.today(),
                    status='appointed',
                    contact_card__isnull=True,
                ) |
                # Keep selected application in list
                models.Q(
                    position__term_from__lte=date.today(),
                    position__term_to__gte=date.today(),
                    status='appointed',
                    applicant=contact_card.application.applicant
                )
            )
        else:
            self.fields['application'].queryset = Application.objects.filter(
                position__term_from__lte=date.today(),
                position__term_to__gte=date.today(),
                status='appointed',
                contact_card__isnull=True,
            )


class ContactBlockForm(WagtailAdminModelForm):

    def __init__(self, *args, **kwargs):
        super(ContactBlockForm, self).__init__(*args, **kwargs)
        contact_card = self.instance
        Application = apps.get_model('involvement', 'Application')

        if contact_card.application:
            self.fields['application'].queryset = Application.objects.filter(
                models.Q(
                    position__term_from__lte=date.today(),
                    position__term_to__gte=date.today(),
                    status='appointed',
                    contact_card__isnull=True,
                ) | # Keep selected application in list
                models.Q(
                    position__term_from__lte=date.today(),
                    position__term_to__gte=date.today(),
                    status='appointed',
                    applicant=contact_card.application.applicant
                )
            )
        else:
            self.fields['application'].queryset = Application.objects.filter(
                position__term_from__lte=date.today(),
                position__term_to__gte=date.today(),
                status='appointed',
                contact_card__isnull=True,
            )


@register_snippet
class ContactCard(models.Model):

    position = models.ForeignKey(
        'Position',
        related_name='contact_cards',
        on_delete=models.CASCADE,
        blank=False,
    )

    application = models.OneToOneField(
        'Application',
        on_delete=models.CASCADE,
        related_name='contact_card',
        blank=True,
        null=True,
    )

    picture = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def __str__(self) -> str:
        if self.application is not None:
            return '%(teams)s | %(position)s - %(applicant)s %(image)s' % {
                'teams': self.position.role.team_names,
                'position': self.position,
                'applicant': self.application.applicant,
                'image': '(%s)' % _('picture missing')
                         if not self.picture else '',
            }

        return '%(teams)s | %(position)s - %(applicant)s' % {
            'teams': self.position.role.team_names,
            'position': self.position,
            'applicant': _('Vacant Position')
        }

    list_filter = ('application__position__role__team')
    base_form_class = ContactBlockForm

        return '%(teams)s | %(position)s - %(applicant)s %(image)s' % {
            'teams': self.position.role.team_names,
            'position': self.position,
            'applicant': _('Vacant Position'),
            'image': '(%s)' % _('picture missing') if not self.picture else '',
        }

    list_filter = ('application__position__role__team')
    base_form_class = ContactBlockForm

    panels = [
        FieldPanel('application'),
        ImageChooserPanel('picture'),
    ]
