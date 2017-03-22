from django.conf.urls import url, include

from members import views

urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(
        r'^email_change_confirm/(?P<token>[0-9A-Za-z]{12})/$',
        views.email_change_confirm,
        name='email_change_confirm'
    ),

    # Views given by django auth library
    url(r'', include('django.contrib.auth.urls')),
]
