from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return JsonResponse(
                {
                 'message': 'Username,password and email are required',
                 'status': 'error'
                },
                status=400)

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {
                 'message': 'Username already exists',
                 'status': 'error'
                },
                status=400)
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {
                 'message': 'Email already exists',
                 'status': 'error'
                },
                status=400)

        # Create user
        user = User.objects.create_user(username=username, password=password)

        return JsonResponse(
            {
                 'message': 'Registration successful',
                 'user_id': user.id
            },
            status=200)

    return JsonResponse(
        {
            'error': 'POST method required',
            'status': 'error'
        }, status=405)

def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    print(username);
    print(password);
    return JsonResponse(
        {
            'message': 'Login endpoint',
            'status': 'error'
        }, status=501)