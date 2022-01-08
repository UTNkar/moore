from django.forms import (ModelForm, BooleanField, IntegerField, ChoiceField,
                          Textarea, CharField)
from events.models import Participant
from utils.validators import SSNValidator


class ParticipantForm(ModelForm):
    name = CharField(max_length=100, required=False)
    person_nr = CharField(max_length=13, validators=[
                          SSNValidator()], required=False)

    def __init__(self, price_list, locked=False, *args, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        for price_field in price_list.fields:
            field = None
            field_type = price_field.get("Type", "")
            field_name = price_field.get("Name", "")
            required = price_field.get("Required", False)
            # TODO: multiple checkboxes
            if field_type == "checkbox":
                field = BooleanField(label=field_name, required=required)
            elif field_type == "text":
                field = CharField(label=field_name,
                                  required=required, max_length=100)
            elif field_type == "long text":
                field = CharField(
                    label=field_name, required=required,
                    max_length=1000, widget=Textarea
                )
            elif field_type == "number":
                field = IntegerField(
                    label=field_name, required=required, disabled=locked)
            elif field_type == "Dropdown":
                field = ChoiceField(
                    label=field_name,
                    choices=[(x, x) for x in price_field.get("Choices")],
                    required=required,
                    disabled=locked)
            if instance:
                initial = instance.order.get(field_name)
                field.initial = initial
            self.fields[field_name] = field

        for field in self.fields:
            if locked:
                self.fields[field].disabled = True

    class Meta:
        model = Participant
        fields = ('name', 'person_nr')

    def clean(self):
        cleaned_data = super(ParticipantForm, self).clean()
        pk = cleaned_data.pop('id', '')
        name = cleaned_data.pop('name', '')
        person_nr = cleaned_data.pop('person_nr', '')

        return {'id': pk,
                'name': name,
                'person_nr': person_nr,
                'order': cleaned_data}
