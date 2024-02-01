from django_hosts import patterns, host
from django.conf import settings

host_patterns = patterns(
    '',
    host(r'', settings.ROOT_URLCONF, name='default'),
    host(r'admin', 'admin.urls', name='admin'),
)
