from django.conf import settings
from django.http import JsonResponse
from datetime import datetime
from dateutil.parser import parse
from urllib.parse import quote
import requests
import json

from google.api import google_calendar_list_events


def view_google_calendar(request, id):
    params = {
        'timeMin': request.GET.get('time_min'),
        'timeMax': request.GET.get('time_max'),
    }

    return JsonResponse(google_calendar_list_events(id, params))
