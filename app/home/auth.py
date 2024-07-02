from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

def validate_token_view(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return JsonResponse({'error': 'No token provided'}, status=400)
    
    token = auth_header.split()[1]
    jwt_auth = JWTAuthentication()

    try:
        validated_token = jwt_auth.get_validated_token(token)
        user = jwt_auth.get_user(validated_token)
        return JsonResponse({'is_valid': True, 'username': user.username})
    except (InvalidToken, TokenError):
        return JsonResponse({'is_valid': False}, status=401)