from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class TokenRefreshView(APIView):
    def post(self, request):
        try:
            # Retrieve the refresh token from cookies
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({'detail': 'Refresh token not found'}, status=status.HTTP_401_UNAUTHORIZED)

            token = RefreshToken(refresh_token)
            new_tokens = {
                'access': str(token.access_token),
                'refresh': str(token)
            }

            # Set new cookies if needed
            response = Response(new_tokens, status=status.HTTP_200_OK)
            response.set_cookie('refresh_token', str(token), httponly=True, secure=True, samesite='Strict')

            return response
        except TokenError as e:
            logger.error(f"Token refresh error: {e}")
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
def verify_token(request):
    access_token = request.COOKIES.get('access_token')  # Get token from cookies
    if not access_token:
        return JsonResponse({"status": "missing"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Verify the token
        AccessToken(access_token)  # This will raise an exception if the token is invalid
        return JsonResponse({"status": "valid"})
    except TokenError as e:
        if "token_expired" in str(e):
            return JsonResponse({"status": "expired"}, status=status.HTTP_401_UNAUTHORIZED)
        return JsonResponse({"status": "invalid"}, status=status.HTTP_401_UNAUTHORIZED)