
# from wagtail.admin import urls as wagtailadmin_urls
# from django.conf.urls import include, url

# urlpatterns = [
#     url(r'', include(wagtailadmin_urls)),
# ]

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', admin.site.urls),
]
