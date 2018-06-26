from datetime import date
from django import forms
from django.apps import apps
from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from utils.translation import TranslatedField


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

    application = models.OneToOneField(
        'Application',
        on_delete=models.CASCADE,
        related_name='contact_card',
        blank=True,
        null=True
    )

    picture = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    description_en = RichTextField(
        verbose_name=_('English Description'),
        blank=True,
    )

    description_sv = RichTextField(
        verbose_name=_('Swedish Description'),
        blank=True,
    )

    description = TranslatedField('description_en', 'description_sv')

    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
        help_text=_('Overrides account name of position holder of the selected'
                    ' role.'),
        blank=True,
    )

    role_text_en = models.CharField(
        max_length=100,
        verbose_name=_('English Role Name'),
        help_text=_('Overrides role name from the selected role.'),
        blank=True,
    )

    role_text_sv = models.CharField(
        max_length=100,
        verbose_name=_('Swedish Role Name'),
        help_text=_('Overrides role name from the selected role.'),
        blank=True,
    )
    role_text = TranslatedField('role_text_en', 'role_text_sv')

    email = models.EmailField(
        verbose_name=_('Email address'),
        help_text=_('Overrides account email address of position holder of the'
                    ' selected role.'),
        blank=True,
    )

    def __str__(self) -> str:
        if self.application:
            return '%(teams)s | %(position)s - %(applicant)s' % {
                'teams': self.application.position.role.team_names,
                'position': self.application.position,
                'applicant': self.application.applicant
            }
        return '%(name)s - %(role)s' % {
            'name': self.name,
            'role': self.role_text
        }

    list_filter = ('application__position__role__team')
    base_form_class = ContactBlockForm

    panels = [
        FieldPanel('application'),
        ImageChooserPanel('picture'),
        FieldPanel('description_en'),
        FieldPanel('description_sv'),
        FieldPanel('name'),
        FieldPanel('role_text_en'),
        FieldPanel('role_text_sv'),
        FieldPanel('email'),
    ]
