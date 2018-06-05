from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from utils.translation import TranslatedField


@register_snippet
class ContactCard(models.Model):
    role = models.OneToOneField(
        'Role',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='contact_cards',
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
        if self.role:
            return self.role.__str__()
        else:
            return '%(name)s - %(role)s' % {
                'name': self.name,
                'role': self.role_text
            }

    panels = [
        FieldPanel('role'),
        ImageChooserPanel('picture'),
        FieldPanel('description_en'),
        FieldPanel('description_sv'),
        FieldPanel('name'),
        FieldPanel('role_text_en'),
        FieldPanel('role_text_sv'),
        FieldPanel('email'),
    ]
