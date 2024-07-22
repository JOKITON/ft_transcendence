from django.http import JsonResponse
from django.middleware.csrf import get_token, CsrfViewMiddleware
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

@csrf_protect
def check_csrf_token(request):
    csrf_token_from_cookie = request.COOKIES.get('csrftoken')

    if not csrf_token_from_cookie:
        return JsonResponse({'status': 'off', 'message': 'No CSRF token found in cookies'})
    
    csrf_middleware = CsrfViewMiddleware(lambda req: None)

    try:
        # Create a mock request to validate the CSRF token
        csrf_middleware.process_view(request, None, (), {})
        return JsonResponse({'status': 'valid', 'csrftoken': csrf_token_from_cookie})
    except Exception as e:
        # If validation fails, clear the CSRF token cookie and request a new token
        response = JsonResponse({'status': 'invalid', 'message': 'Invalid CSRF token'})
        response.delete_cookie('csrftoken')
        return response

@ensure_csrf_cookie
def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response