from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from events.models import Participant

class ParticipantDelete(DeleteView):
    model = Participant
