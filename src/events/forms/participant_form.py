from django.forms import (MultiValueField, MultiWidget, ModelForm, BaseModelFormSet, BooleanField, IntegerField, ChoiceField,
                          TextInput, NumberInput, CheckboxInput, Select, CharField)
from events.models import Participant
from utils.validators import SSNValidator
from django.core.exceptions import ValidationError

class ParticipantForm(ModelForm):
    name = CharField(max_length=100, required=False)
    person_nr = CharField(max_length=13, validators=[SSNValidator()], required=False)

    def __init__(self, price_list, *args, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        for price_field in price_list.fields:
            field = None
            field_type = price_field.get("Type")
            field_name = price_field.get("Name")
            # TODO: multiple checkboxes, free text field
            if field_type == "checkbox":
                field = BooleanField(label=field_name, required=False)
            elif field_type == "number":
                field = IntegerField(label=field_name, required=False)
            elif field_type == "Dropdown":
                field = ChoiceField(label=field_name, choices=[(x, x) for x in price_field.get("Choices")], required=False)
            if instance:
                initial = instance.order.get(field_name)
                field.initial = initial
            self.fields[field_name] = field

    class Meta:
        model = Participant
        fields = ('name', 'person_nr')

    def clean(self):
        cleaned_data = super(ParticipantForm, self).clean()
        pk = cleaned_data.pop('id', '')
        name = cleaned_data.pop('name', '')
        person_nr = cleaned_data.pop('person_nr', '')

        return {'id': pk, 'name': name, 'person_nr': person_nr, 'order': cleaned_data}
