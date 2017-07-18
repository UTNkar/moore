from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BrandingConfig(AppConfig):
    name = 'branding'
    verbose_name = _('Branding')
