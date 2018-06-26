from wagtail.contrib.forms.models import AbstractFormField
from modelcluster.fields import ParentalKey


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')
