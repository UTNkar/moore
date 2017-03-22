from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MembersConfig(AppConfig):
    name = 'members'
    verbose_name = _('UTN Member Management')

    def ready(self):
        import members.signals #noqa