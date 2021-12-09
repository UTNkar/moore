from django.forms import (MultiValueField, MultiWidget, ModelChoiceField, IntegerField, ChoiceField,
                          TextInput, NumberInput, CheckboxInput, Select, CharField, ModelForm)
from events.models import Assignment
from utils.validators import SSNValidator
from django.core.exceptions import ValidationError

class EventAssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        exclude = ['id']
