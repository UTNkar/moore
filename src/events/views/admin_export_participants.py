import csv
from django.shortcuts import get_object_or_404
from django.utils import timezone as tz
from django.http import HttpResponse
from events.models import Participant, Event


def admin_export_participants(request, pos_id=None):
    event = get_object_or_404(Event, pk=pos_id)
    participants = Participant.objects.filter(ticket__event=event)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        'attachment;filename='
        + str(event)
        + '_'
        + str(tz.now())
        + "_participants.csv")

    price_list_fields = event.price_list.fields
    columns = (["name", "person_nr"]
               + [field['Name'] for field in price_list_fields]
               + ["ticket_number", "cost"])

    writer = csv.writer(response)
    writer.writerow(columns)

    for participant in participants:
        writer.writerow(
            [participant.name,
             participant.person_nr]
            + [participant.order.get(field['Name'], None)
               for field in price_list_fields]
            + [participant.ticket.ticket_number,
                participant.calculate_order_cost()]
        )

    return response
