from django.conf import settings
from django_hosts.resolvers import reverse_host
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin
import re


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


class TrustedHostMiddleware(MiddlewareMixin):
    """
    Middleware to dynamically set the HTTP_HOST from a set of HTTP headers,
    ensuring it matches the allowed hosts in settings.ALLOWED_HOSTS.
    """

    def __call__(self, request):
        current_host = request.META.get('HTTP_HOST', '')
        if (current_host and self.is_allowed_host(current_host)):
            return self.get_response(request)

        headers_to_check = [
            ('HTTP_X_FORWARDED_HOST', 'X-Forwarded-Host'),
            ('HTTP_HOST', 'Host'),
            ('HTTP_ORIGIN', 'Origin'),
            ('HTTP_REFERER', 'Referer')
        ]

        host_name = None
        for meta_key, header in headers_to_check:
            # Prefer META if defined; fallback to request.headers
            host_value = (request.META.get(meta_key)
                          or request.headers.get(header, ''))
            # Extract the hostname, excluding protocol and path.
            host_name = self.extract_hostname(host_value)
            if host_name and self.is_allowed_host(host_name):
                request.META['HTTP_HOST'] = host_name
                break
            host_name = None

        if not host_name:
            # Fallback to using host from request URL if no matching header
            fallback_host = (request.build_absolute_uri()
                             .split('//')[1].split('/')[0])
            fallback_host_name = self.extract_hostname(fallback_host)
            if self.is_allowed_host(fallback_host_name):
                request.META['HTTP_HOST'] = fallback_host_name

        return self.get_response(request)

    def extract_hostname(self, value):
        """
        Extracts hostname from a URL, ignoring protocol, port, and path.
        """
        # Regex captures hostname from start of string or after protocol.
        # It stops at port delimiter ":" or path delimiter "/".
        match = re.search(r'^(?:https?://)?([^:/]+)', value)
        return match.group(1) if match else ''

    def is_allowed_host(self, host):
        """
        Checks if a host matches any pattern in ALLOWED_HOSTS.
        """
        # Loop through ALLOWED_HOSTS to see if the host matches any pattern.
        # Patterns starting with '.' match any subdomain.
        for allowed_host in settings.ALLOWED_HOSTS:
            if allowed_host.startswith('.'):
                domain = allowed_host[1:]
                if host.endswith('.' + domain) or host == domain[1:]:
                    return True
            elif host == allowed_host:  # Exact match
                return True
        return False
