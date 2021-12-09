from django.shortcuts import render, get_object_or_404
from django.forms import modelformset_factory
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.db.models import Model
from events.models import Event, Ticket, EventApplication, Participant
from events.forms import ParticipantForm
from django.contrib.auth.decorators import login_required

@login_required
def my_ticket(request, event_pk):
    """View for a single ticket"""
    context = {}
    try:
        ticket = Ticket.objects.get(owner=request.user.id, event=event_pk)
        event = Event.objects.get(id=event_pk)
        ParticipantFormset = modelformset_factory(Participant, form=ParticipantForm, max_num=ticket.event.num_participants_per_ticket, extra=0) # arbitrary high number
        queryset = Participant.objects.filter(ticket=ticket)
        max_num_participant = queryset.count() == ticket.event.num_participants_per_ticket

        if request.method == "POST":

            if "add_participant" in request.POST and not max_num_participant:
                new_participant = Participant(ticket=ticket)
                new_participant.ticket = ticket
                new_participant.save()
                queryset = Participant.objects.filter(ticket=ticket)
                formset = ParticipantFormset(queryset=queryset, initial=queryset, form_kwargs={'price_list': event.price_list})

            formset = ParticipantFormset(request.POST, request.FILES, form_kwargs={'price_list': event.price_list})

            if formset.is_valid():
                for form in formset:
                    if form.is_valid():
                        instance = form.save(commit=False)
                        delete = "delete_{}".format(instance.id)
                        if delete in request.POST:
                            instance.delete()
                        else:
                            cleaned_data = form.cleaned_data
                            instance.order = cleaned_data['order']
                            instance.save()
                queryset = Participant.objects.filter(ticket=ticket)
                formset = ParticipantFormset(queryset=queryset, initial=queryset, form_kwargs={'price_list': event.price_list})
        else:
            formset = ParticipantFormset(queryset=queryset, form_kwargs={'price_list': event.price_list})

        context['ticket'] = ticket
        context['participants_formset'] = formset
        context['max_num_participants'] = max_num_participant
    except ValueError:
        pass

    return render(request, 'events/my_ticket.html', context)
