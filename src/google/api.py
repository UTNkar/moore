from django.conf import settings
from dateutil.parser import parse
from urllib.parse import quote
import requests
import json

def google_calendar_list_events(id, params):
    params['key'] = settings.GOOGLE_API_KEY,

    url = 'https://www.googleapis.com/calendar/v3/calendars/%s/events' \
            % quote(id, safe="%/:=~+!$,;'@()*[]")
    response = requests.get(url, params=params)
    result = response.json()
    items = []
    if 'items' in result:
        for item in result['items']:
            start_date = parse(item['start']['dateTime']) \
                if 'dateTime' in item['start'] \
                else parse(item['start']['date'])

            end_date = parse(item['end']['dateTime']) \
                if 'dateTime' in item['end'] \
                else parse(item['end']['date'])

            items.append({
                'id': item['id'],
                'summary': item.get('summary'),
                'description': item.get('description'),
                'day': start_date.strftime('%d'),
                'month': start_date.strftime('%b'),
                'start_date': start_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'end_date': end_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            })

    data = {
        'id': id,
        'items': items,
    }
    return data


def youtube_search(params):
    params['key'] = settings.GOOGLE_API_KEY,

    response = requests.get(
        'https://www.googleapis.com/youtube/v3/search',
        params=params
    )
    json = response.json()

    items = json['items'] if 'items' in json else []
    for item in items:
        video_id = item['id']['videoId']
        url = 'https://www.youtube.com/embed/%s?showinfo=0&autoplay=0&rel=0' \
                % video_id
        item['embed_url'] = url

    return items
