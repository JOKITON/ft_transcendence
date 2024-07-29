import requests
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class TokenValidationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.headers.get('Authorization')
        
        if not token:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)

        api_url = 'http://api:8000/api/user/token/verify/'  # Endpoint for token verification
        headers = {'Authorization': token}
        token = token.split(' ')[1]
        payload = {'token': token}

        try:
            response = requests.post(api_url, headers=headers, json=payload)
            if response.status_code == 200:
                # Token is valid
                return None  # Continue processing the request
            else:
                # Token is invalid
                return JsonResponse({'error': 'Invalid token'}, status=401)
        except requests.RequestException:
            return JsonResponse({'error': 'Error verifying token'}, status=500)
