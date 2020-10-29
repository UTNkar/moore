from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GoogleConfig(AppConfig):
    name = 'google'
    verbose_name = _('Google')
