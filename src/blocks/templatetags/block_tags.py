from django import template
from datetime import date
from google.api import google_calendar_list_events, youtube_search
from google.models import GoogleCalendarPage
from wagtail.core.models import Page

register = template.Library()


@register.inclusion_tag('blocks/tags/facebook.html')
def facebook(app_id, page_name, size):

    data = {
        'app_id': app_id,
        'page_name': page_name,
        'size': size,
    }

    return data


@register.inclusion_tag('blocks/tags/youtube.html')
def youtube(channel_id, size):

    params = {
        'maxResults': 1,
        'part': 'snippet',
        'order': 'date',
        'channelId': channel_id,
    }

    items = youtube_search(params)

    url = items[0]['embed_url'] if len(items) else ''

    data = {
        'size': size,
        'url': url,
    }

    return data


@register.inclusion_tag('blocks/tags/calendar.html')
def calendar(id, size):

    params = {
        'maxResults': 4,
        'timeMin': date.today().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
    }

    data = google_calendar_list_events(id, params)
    data['size'] = size

    page = Page.objects.type(GoogleCalendarPage).first()
    data['calendar_url'] = page.get_url() if page else ''

    return data
