# __author__ = "Aditi Sharma"

from django.http import QueryDict

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class HttpPostTunnelingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'HTTP_X-METHODOVERRIDE' in request.META:
            http_method = request.META['HTTP_X-METHODOVERRIDE']
            if http_method.lower() == 'delete':
                request.method = 'DELETE'
                request.META['REQUEST_METHOD'] = 'DELETE'
                request.DELETE = QueryDict(request.body)
        return None
