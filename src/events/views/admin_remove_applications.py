from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.forms import Form, NumberInput
from rules.contrib.views import permission_required
from utils.view_utils import get_position_by_pk
from events.models import Event, Ticket, EventApplication
from django.forms import modelformset_factory, IntegerField
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from events.forms import EventAssignmentForm
from events.models import Participant, EventApplication

def admin_remove_applications(request, pos_id=None):
    """
    Admin view to appoint members to the position
    """
    event = get_object_or_404(Event, pk=pos_id)
    applications = EventApplication.objects.filter(event=event)

    if request.method == 'POST':
        if 'confirm' in request.POST:
            applications.delete()

    view = {
        'get_meta_title': 'Remove applications',
        'get_page_title': 'Remove applications for',
        'get_page_subtitle': event.__str__(),
        'header_icon': 'pick',
    }
    context = {
        'view': view,
        'request': request,
        'event': event,
        'applications': applications
    }
    return render(request, 'events/admin/event_remove_applications.html',
                  context)
