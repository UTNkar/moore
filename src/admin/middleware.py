from django.conf import settings
from django_hosts.resolvers import reverse_host
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin


class RedirectAdminMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest) -> HttpResponse:
        if (request.path.startswith('/admin/') and
                request.method == 'GET' and
                request.headers.get('Accept', '').startswith('text/html')):
            protocol = 'https' if request.is_secure() else 'http'
            host = reverse_host('admin')
            if getattr(settings, 'HOST_PORT', None):
                host = f"{host}:{settings.HOST_PORT}"
            path = request.path[7:]  # Remove '/admin/'
            return HttpResponseRedirect(f'{protocol}://{host}/{path}')
        return None
