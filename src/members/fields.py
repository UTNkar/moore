from django import forms
from phonenumbers import parse, is_valid_number
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str
from utils.validators import SSNValidator


class PhoneNumberField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(PhoneNumberField, self).__init__(
            *args, label=_('Phone number'), **kwargs
        )

    def clean(self, phonenumber):
        try:
            parsed_phone = parse(phonenumber, "SE")
            if not is_valid_number(parsed_phone):
                raise Exception

            return phonenumber
        except Exception:
            raise forms.ValidationError(_("Invalid phonenumber"))


class PersonNumberField(forms.Field):
    def __init__(self, *args, **kwargs):
        super(PersonNumberField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return None, ''
        value = force_str(value).strip()
        SSNValidator()(value)
        return value

    def widget_attrs(self, widget):
        attrs = super(PersonNumberField, self).widget_attrs(widget)
        attrs['class'] = attrs.get('class', '') + ' person_number'
        attrs['placeholder'] = 'YYYYMMDD-XXXX'
        return attrs
