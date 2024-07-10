from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@csrf_protect
def refresh_token_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'You\'re not logged in.'}, status=400)
    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token is None:
        return Response({'detail': 'Refresh token not found'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)

        response = Response({'detail': 'Token refreshed successfully'}, status=status.HTTP_200_OK)
        response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Lax')

        return response
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
