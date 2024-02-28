from django.conf import settings
from django_hosts.resolvers import reverse_host
from django.http import HttpResponseRedirect, HttpResponseNotAllowed


def redirect_admin(request, path):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    elif request.headers.get('Accept') == 'application/json':
        return HttpResponseNotAllowed(['GET'])

    protocol = 'https' if request.is_secure() else 'http'
    host = reverse_host(host='admin')
    if getattr(settings, 'HOST_PORT', None):
        host = f"{host}:{settings.HOST_PORT}"
    return HttpResponseRedirect(f'{protocol}://{host}/{path}')
