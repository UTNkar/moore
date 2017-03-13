from django.conf.urls import url, include

from members import views

urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),

    # Views given by django auth library
    url(r'', include('django.contrib.auth.urls')),
]
