from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.forms import Form, NumberInput
from rules.contrib.views import permission_required
from utils.view_utils import get_position_by_pk
from events.models import Event, Ticket, EventApplication
from django.forms import modelformset_factory, IntegerField, ChoiceField
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from events.forms import EventAssignmentForm


def random_assignment(event, num_to_assign, priority):
    """Randomly assigns a number of applications to empty tickets"""
    user_model = get_user_model()

    # First, find all tickets with owners and disqualify those owners.
    assigned_tickets = Ticket.objects.exclude(event=event, owner=None)
    applicants_without_tickets = user_model.objects.exclude(ticket__in=assigned_tickets, status=priority)

    # Then, take applications made by those without tickets in random order, and take the first num_to_assign
    random_applications = EventApplication.objects.filter(event_applicant__in=applicants_without_tickets).order_by('?')[:num_to_assign]
    unassigned_tickets = Ticket.objects.filter(event=event, owner=None).order_by('ticket_number')

    for ticket, application in zip(unassigned_tickets, random_applications):
        # assign them
        ticket.owner = application.event_applicant


    return unassigned_tickets

class NumToRandomizeForm(Form):
    number_to_randomly_assign = IntegerField(initial=0)

    choices = (('member', 'UTN members'),
               ('nonmember', 'Non UTN members'))

    preference = ChoiceField(choices=choices)

def admin_assign(request, pos_id=None):
    """
    Admin view to appoint members to the position
    """
    event = get_object_or_404(Event, pk=pos_id)
    num_to_randomize = 0
    assignments = []
    formset = modelformset_factory(Ticket, extra=0, max_num=num_to_randomize, fields=['ticket_number', 'owner'])
    ticket_formset = formset(queryset=Ticket.objects.none())
    num_randomize_form = NumToRandomizeForm(prefix='num_assign')
    disabled = True

    if request.method == 'POST':
        ticket_formset = formset(request.POST, request.FILES)
        num_randomize_form = NumToRandomizeForm(request.POST, request.FILES, prefix='num_assign')

        if ticket_formset.is_valid() and num_randomize_form.is_valid():
            cleaned_data = formset.cleaned_data
            num_to_randomize = num_randomize_form.cleaned_data.get('number_to_randomly_assign', 0)
            priority = num_randomize_form.cleaned_data.get('preference', 'member')
            if 'randomize' in request.POST:
                formset = modelformset_factory(Ticket, extra=0, max_num=num_to_randomize, fields=['ticket_number', 'owner'])
                assignments = random_assignment(event, num_to_randomize, priority)
                disabled = False if num_to_randomize > 0 and assignments.count() > 0 else True
                ticket_formset = formset(queryset=assignments)
            elif 'save' in request.POST:
                instances = ticket_formset.save()
                ticket_formset = formset(queryset=Ticket.objects.none())

    view = {
        'get_meta_title': 'Assign tickets',
        'get_page_title': 'Assign tickets for',
        'get_page_subtitle': event.__str__(),
        'header_icon': 'pick',
    }
    context = {
        'view': view,
        'request': request,
        'event': event,
        'formset': ticket_formset,
        'num_randomize_form': num_randomize_form,
        'disabled': disabled
    }
    return render(request, 'events/admin/event_assignment.html',
                  context)
