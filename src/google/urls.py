from django.conf.urls import re_path
from google import views


urlpatterns = [
    re_path(
        r'^api/google/calendar/(?P<id>.*)$',
        views.view_google_calendar,
        name='view_google_calendar',
    ),
]
