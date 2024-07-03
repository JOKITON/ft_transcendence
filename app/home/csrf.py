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

def csrf_token_view(request):
    csrf_token = get_token(request)  # Fetch the CSRF token
    response = JsonResponse({'csrf_token': csrf_token})
    response.set_cookie('csrftoken', csrf_token, httponly=True, secure=True)
    return response