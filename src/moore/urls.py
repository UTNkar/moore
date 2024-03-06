from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.urls import path

from search import views as search_views
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.admin import urls as wagtailadmin_urls

from .api import api_router
from .urls_utils import delete_urls

from members.views import member_check_api

urlpatterns = [
    # Needs to be imported before wagtail urls
    url(r'^api/', api_router.urls),

    url(r'', include('involvement.urls')),
    url(r'', include('events.urls')),
    path('member_check_api/', member_check_api, name='member_check_api'),

    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),

    url(r'^accounts/', include('members.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'', include('google.urls')),

    path('instagram/', include('instagram.urls')),

    # We need to include the `wagtailadmin_urls` to support `reverse`.
    # Unless running tests, /admin/* will redirect to admin.x/*.
    url(r'^admin/', include(wagtailadmin_urls)),

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

# We remove the /admin redirect
# if running tests in order to make writing tests easier.
if settings.IS_RUNNING_TEST:
    urlpatterns = delete_urls(
        urlpatterns,
        delete_name='wagtailadmin_redirect'
    )
