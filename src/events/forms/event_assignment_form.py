from django.forms import ModelForm
from events.models import Assignment


class EventAssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        exclude = ['id']
