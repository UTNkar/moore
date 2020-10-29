from django.conf.urls import re_path, include
from django.urls import reverse_lazy
from django.views.generic import CreateView

from members import views
from members.forms import RegistrationForm

urlpatterns = [
    re_path(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    re_path(
        r'^email_change_confirm/(?P<token>[0-9A-Za-z]{12})/$',
        views.email_change_confirm,
        name='email_change_confirm'
    ),
    re_path('^register/', CreateView.as_view(
        template_name='members/register.html',
        form_class=RegistrationForm,
        success_url=reverse_lazy('login'),
    ), name='register'),

    # Views given by django auth library
    re_path(r'', include('django.contrib.auth.urls')),
    re_path(
        r'password_reset_custom/',
        views.CustomPasswordResetView.as_view(),
        name='password_reset_custom'),
]
