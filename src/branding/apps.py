from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BrandingConfig(AppConfig):
    name = 'branding'
    verbose_name = _('Branding')
