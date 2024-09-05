import requests
from django.http import JsonResponse

class TokenVerifyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self.verify_token(request):
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        return self.get_response(request)

    def verify_token(self, request):
        # Extract the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False
        
        token = auth_header.split(' ')[1]  # Get the token part

        # Verify the token with the external API
        try:
            api_url = 'http://api:8000/api/user/token/verify/'  # Endpoint for token verification
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.post(api_url, headers=headers, json={'token': token})
            return response.status_code == 200
        except requests.RequestException:
            return False
