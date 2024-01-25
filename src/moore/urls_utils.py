from __future__ import absolute_import, unicode_literals

from django.urls.resolvers import URLResolver


def insert_urls_before(urlpatterns: list, before_name: str, url: URLResolver):
    for index, pattern in enumerate(urlpatterns):
        # Insert before index if `name` or `app_name` matches
        if hasattr(pattern, 'name'):
            if pattern.name == before_name:
                urlpatterns.insert(index, url)
                break
        elif hasattr(pattern, 'app_name'):
            if pattern.app_name == before_name:
                urlpatterns.insert(index, url)
                break

    return urlpatterns


def delete_urls(urlpatterns: list, delete_name: str):
    for index, pattern in enumerate(urlpatterns):
        if hasattr(pattern, 'name'):
            if pattern.name == delete_name:
                # Insert before index
                urlpatterns.pop(index)
                break

    return urlpatterns
