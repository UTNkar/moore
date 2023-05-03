from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from jsonschemaform.admin.widgets.jsonschema_widget import JSONSchemaWidget

schema = {
    "title": "Price list",
    "description": "Each entry in this list is considered an orderable item.",
    "type": "array",
    "format": "table",
    "items": {
        "type": "object",
        "properties": {
            "Name": {"type": "string"},
            "Price": {"type": "integer"},
            "Non-member price": {"type": "integer"},
            "Type": {
                "type": "string",
                "default": "Checkbox",
                "enum": ["text", "long text", "number", "checkbox", "Dropdown"]
            },
            "Choices": {
                "type": "array",
                "format": "table",
                "items": {
                    "type": "string",
                },
                "description": "These are only in effect "
                               "if the type of choice is Dropdown"
            },
            "Required": {
                "type": "checkbox"
            }
        }
    }
}


class Costs(models.Model):
    name = models.CharField(
        help_text=_('This field identifies the cost list.'),
        verbose_name=_('Cost list name'),
        max_length=255
    )

    fields = models.JSONField(
        help_text=_('These fields determine what each participant can '
                    'purchase. They each need their name (key) and '
                    'field type.'),
        verbose_name=_('Purchaseable items'))

    panels = [MultiFieldPanel([
        FieldPanel('name'),
        FieldPanel('fields', widget=JSONSchemaWidget(schema))
    ])]

    class Meta:
        verbose_name = _('Costs')
        verbose_name_plural = _('Costs')
        ordering = ['name']

    def __str__(self):
        return self.name
