from django.conf.urls import url, include
from django.urls import reverse_lazy
from django.views.generic import CreateView

from members import views
from members.forms import RegistrationForm

urlpatterns = [
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(
        r'^email_change_confirm/(?P<token>[0-9A-Za-z]{12})/$',
        views.email_change_confirm,
        name='email_change_confirm'
    ),
    url('^register/', CreateView.as_view(
        template_name='members/register.html',
        form_class=RegistrationForm,
        success_url=reverse_lazy('login'),
    ), name='register'),

    # Views given by django auth library
    url(r'', include('django.contrib.auth.urls')),
]
