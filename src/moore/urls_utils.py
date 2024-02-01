from __future__ import absolute_import, unicode_literals


def delete_urls(urlpatterns: list, delete_name: str):
    for index, pattern in enumerate(urlpatterns):
        if hasattr(pattern, 'name'):
            if pattern.name == delete_name:
                # Insert before index
                urlpatterns.pop(index)
                break

    return urlpatterns
