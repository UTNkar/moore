from django.http import JsonResponse
from google.api import google_calendar_list_events


def view_google_calendar(request, id):
    params = {
        'timeMin': request.GET.get('time_min'),
        'timeMax': request.GET.get('time_max'),
    }

    return JsonResponse(google_calendar_list_events(id, params))
