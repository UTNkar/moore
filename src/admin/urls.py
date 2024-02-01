from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from wagtail.admin import urls as wagtailadmin_urls

from moore.urls import urlpatterns as base_urlpatterns

# Use the same `urlpatterns` as other domains as the base
urlpatterns = base_urlpatterns.copy()

# Insert `wagtailadmin_urls` at appropriate level
urlpatterns.insert(
    len(urlpatterns) - 3,
    url(r'', include(wagtailadmin_urls))
)
