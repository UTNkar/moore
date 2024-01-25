from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from wagtail.core import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from moore.urls import urlpatterns as base_urlpatterns

# Use the same `urlpatterns` as other domains as the base
urlpatterns = base_urlpatterns.copy()

# Append `wagtailadmin_urls` before `wagtail_urls`
for index, pattern in enumerate(urlpatterns):
    if hasattr(pattern, 'url_patterns'):
        if wagtail_urls.urlpatterns == pattern.url_patterns:
            # Insert the new_pattern before the wagtail include
            urlpatterns.insert(index, url(r'', include(wagtailadmin_urls)))
            break
