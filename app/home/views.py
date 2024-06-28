from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        # Create user
        user = User.objects.create_user(username=username, password=password)

        return JsonResponse({'message': 'Registration successful', 'user_id': user.id}, status=200)

    return JsonResponse({'error': 'POST method required'}, status=405)

def login_view(request):
    return JsonResponse({'message': 'Login endpoint, but not implemented yet'}, status=501)