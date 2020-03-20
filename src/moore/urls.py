from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url

from search import views as search_views
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from .api import api_router

urlpatterns = [

    # Needs to be imported before wagtail urls
    url(r'^api/', api_router.urls),

    # Needs to be imported before wagtail admin
    url(r'', include('involvement.urls')),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),

    url(r'^accounts/', include('members.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'', include('google.urls')),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
