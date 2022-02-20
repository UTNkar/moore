from django.shortcuts import render, get_object_or_404
from django.forms import Form
from events.models import Event, Ticket, EventApplication
from django.forms import modelformset_factory, IntegerField, ChoiceField
from random import shuffle


def random_assignment(event, num_to_assign, priority):
    """Randomly assigns a number of applications to empty tickets"""
    random_applications = (list(
            EventApplication.objects.filter(ticket=None)
        ))

    shuffle(random_applications)
    random_applications = random_applications[:num_to_assign]

    unassigned_tickets = Ticket.objects.filter(
        event=event, owner=None).order_by('ticket_number')[:num_to_assign]

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
    formset = modelformset_factory(
        Ticket, extra=0, max_num=num_to_randomize,
        fields=['ticket_number', 'owner']
    )
    ticket_formset = formset(queryset=Ticket.objects.none())
    num_randomize_form = NumToRandomizeForm(prefix='num_assign')
    disabled = True

    if request.method == 'POST':
        ticket_formset = formset(request.POST, request.FILES)
        num_randomize_form = NumToRandomizeForm(
            request.POST, request.FILES, prefix='num_assign')

        if ticket_formset.is_valid() and num_randomize_form.is_valid():
            num_to_randomize = num_randomize_form.cleaned_data.get(
                'number_to_randomly_assign', 0)
            priority = num_randomize_form.cleaned_data.get(
                'preference', 'member')
            if 'randomize' in request.POST:
                formset = modelformset_factory(
                    Ticket, extra=0, max_num=num_to_randomize,
                    fields=['ticket_number', 'owner']
                )
                assignments = random_assignment(
                    event, num_to_randomize, priority)

                if num_to_randomize > 0 and assignments.count() > 0:
                    disabled = False

                ticket_formset = formset(queryset=assignments)
            elif 'save' in request.POST:
                tickets = ticket_formset.save()

                for ticket in tickets:
                    application = EventApplication.objects.get(
                        event_applicant=ticket.owner,
                        event=ticket.event
                    )
                    application.ticket = ticket
                    application.save()

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
