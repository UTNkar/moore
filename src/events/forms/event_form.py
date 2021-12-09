from django import forms
from django.utils.translation import gettext_lazy as _
from events.models import Event

class EventForm(forms.ModelForm):
    # This is intentionally left empty as it's used for a button which just says "apply"
    # Used for applying to an event.
    class Meta:
        model = Event
        fields = []
