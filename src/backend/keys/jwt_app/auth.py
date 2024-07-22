from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.conf import settings
from django.http import JsonResponse
from django.views import View

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200 and 'access' in response.data:
            access_token = response.data['access']
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=access_token,
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
        return response

class PublicKeyView(View):
    def get(self, request):
        with open('/usr/src/app/secrets/jwt_auth_public.pem', 'r') as f:
            public_key = f.read()
        return JsonResponse({'public_key': public_key})
    
class PrivateKeyView(View):
    def get(self, request):
        with open('/usr/src/app/secrets/jwt_auth_private.pem', 'r') as f:
            private_key = f.read()
        return JsonResponse({'private_key': private_key})