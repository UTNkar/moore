from django.shortcuts import render
from django.forms import modelformset_factory
from django.utils import timezone as tz
from events.models import Event, Ticket, Participant
from events.forms import ParticipantForm
from django.contrib.auth.decorators import login_required

import swish

@login_required
def my_ticket(request, event_pk):
    """View for a single ticket"""
    context = {}
    ticket = Ticket.objects.filter(
        owner=request.user.id, event=event_pk)[0]
    event = Event.objects.get(id=event_pk)
    ParticipantFormset = modelformset_factory(
        Participant, form=ParticipantForm,
        max_num=ticket.event.num_participants_per_ticket, extra=0)
    queryset = Participant.objects.filter(ticket=ticket).order_by('id')
    max_num_participant = (queryset.count() ==
                           ticket.event.num_participants_per_ticket)

    if not ticket.locked and request.method == "POST":
        if "add_participant" in request.POST and not max_num_participant:
            new_participant = Participant(ticket=ticket)
            new_participant.ticket = ticket
            new_participant.save()
            queryset = Participant.objects.filter(
                ticket=ticket).order_by('id')
            formset = ParticipantFormset(
                queryset=queryset, initial=queryset, form_kwargs={
                    'price_list': event.price_list, "locked": ticket.locked
                }
            )

        formset = ParticipantFormset(
            request.POST, request.FILES,
            form_kwargs={'price_list': event.price_list}
        )

        if formset.is_valid():
            for index, form in enumerate(formset):
                if form.is_valid():
                    instance = form.save(commit=False)
                    delete = "delete_{}".format(instance.id)
                    # Check for 0 here to prevent tampering
                    if delete in request.POST and index != 0:
                        instance.delete()
                    elif 'lock_for_payment' in request.POST:
                        ticket.locked = True
                        ticket.total_payment = event.base_price + \
                        sum([participant.calculate_order_cost()
            for participant in queryset])
                        instance.save()
                    else:
                        cleaned_data = form.cleaned_data
                        instance.order = cleaned_data['order']
                        instance.save()
            queryset = Participant.objects.filter(
                ticket=ticket).order_by('id')
            formset = ParticipantFormset(
                queryset=queryset, initial=queryset,
                form_kwargs={'price_list': event.price_list,
                             "locked": ticket.locked}
            )
            # This makes sure that the tickets post_save is called,
            # so that the first user can't be tampered with.
            ticket.save()
    else:
        # Swish grejer
        swish_client = swish.SwishClient(
            environment=swish.Environment.Test,
            merchant_swish_number='1231181189',
            cert=('../swish_certificates/Swish_Merchant_TestCertificate_1234679304.pem', '../swish_certificates/Swish_Merchant_TestCertificate_1234679304.pem'),
            verify='../swish_certificates/Swish_TLS_RootCA.pem'
        )

        payment = swish_client.create_payment(
            payee_payment_reference='0123456789',
            callback_url='https://example.com/api/swishcb/paymentrequests',
            payer_alias='46712345678',
            amount=100,
            currency='SEK',
            message='Kingston USB Flash Drive 8 GB'
        )

        print(payment)

        formset = ParticipantFormset(
            queryset=queryset,
            form_kwargs={'price_list': event.price_list,
                         "locked": ticket.locked}
        )

    # Set this as the first user has to be the owner.
    formset[0].fields['person_nr'].disabled = True
    cost = event.base_price + \
        sum([participant.calculate_order_cost()
            for participant in queryset])
    context['ticket'] = ticket
    context['cost'] = cost
    context['participants_formset'] = formset
    context['max_num_participants'] = max_num_participant
    context['last_payment_date'] = event.last_payment_date
    context['can_still_pay'] = event.last_payment_date > tz.now(
    ) if event.last_payment_date else False

    return render(request, 'events/my_ticket.html', context)
