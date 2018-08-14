from django.conf.urls import url
from google import views


urlpatterns = [
    url(r'^api/google/calendar/(?P<id>.*)$',
        views.view_google_calendar,
        name='view_google_calendar',
    ),
]