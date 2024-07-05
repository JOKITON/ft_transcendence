from urllib import response
from django.shortcuts import render
from django.http import JsonResponse
import json
from django.middleware.csrf import get_token, CsrfViewMiddleware
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt

def check_csrf_token(request):
    csrf_token_from_cookie = request.COOKIES.get('csrftoken')

    if csrf_token_from_cookie:
        # Return a response indicating that the token is valid
        return JsonResponse({'csrftoken': csrf_token_from_cookie})
    else:
        return JsonResponse({'status': 'off'})

@csrf_exempt
@ensure_csrf_cookie
def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response