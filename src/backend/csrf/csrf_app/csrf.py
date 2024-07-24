# csrf.py
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token, CsrfViewMiddleware
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views import View
import requests

@csrf_protect
def check_csrf_token(request):
    csrf_token_from_cookie = request.COOKIES.get('csrftoken')
    csrf_token_from_header = request.META.get('HTTP_X_CSRFTOKEN')

    if not csrf_token_from_cookie:
        return JsonResponse({'status': 'off', 'message': 'No CSRF token found in cookies'})
    
    csrf_middleware = CsrfViewMiddleware(lambda req: None)

    try:
        csrf_middleware.process_view(request, None, (), {})
        return JsonResponse({'status': 'valid', 'csrftoken': csrf_token_from_cookie})
    except Exception:
        response = JsonResponse({'status': 'invalid', 'message': 'Invalid CSRF token'})
        response.delete_cookie('csrftoken')
        return response

@ensure_csrf_cookie
def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response

class ProxyView(View):
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.handle_request(request)

    def put(self, request, *args, **kwargs):
        return self.handle_request(request)

    def delete(self, request, *args, **kwargs):
        return self.handle_request(request)

    def patch(self, request, *args, **kwargs):
        return self.handle_request(request)

    def handle_request(self, request):
        csrf_middleware = CsrfViewMiddleware()
        if csrf_middleware.process_view(request, None, (), {}):
            return JsonResponse({'detail': 'Invalid CSRF token'}, status=403)

        service_url = self.get_service_url(request.path)
        if not service_url:
            return JsonResponse({'detail': 'Service URL not found'}, status=404)

        headers = self.get_headers(request)
        response = requests.request(
            method=request.method,
            url=service_url,
            headers=headers,
            data=request.body
        )

        return HttpResponse(response.content, status=response.status_code, content_type=response.headers.get('Content-Type'))

    def get_service_url(self, path):
        service_mapping = {
            '/api/pong/': 'http://pong:8000',
            # Add more mappings as needed
        }
        for prefix, target in service_mapping.items():
            if path.startswith(prefix):
                return target + path
        return None

    def get_headers(self, request):
        headers = {key: value for key, value in request.headers.items() if key.startswith('HTTP_')}
        headers['Content-Type'] = request.content_type
        return headers
