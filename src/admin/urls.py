
from wagtail.admin import urls as wagtailadmin_urls
from django.urls import path, include

urlpatterns = [
    path(r'', include(wagtailadmin_urls)),
]
