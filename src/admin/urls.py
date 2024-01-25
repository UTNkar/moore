from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from wagtail.admin import urls as wagtailadmin_urls

from moore.urls import urlpatterns as base_urlpatterns
from moore.urls_utils import insert_urls_before

# Use the same `urlpatterns` as other domains as the base
urlpatterns = base_urlpatterns.copy()

# Insert `wagtailadmin_urls` before `wagtail_urls`
urlpatterns = insert_urls_before(
    urlpatterns,
    before_name='wagtail_urls',
    url=url(r'', include(wagtailadmin_urls))
)
