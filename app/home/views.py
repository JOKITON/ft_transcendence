from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json

# CSRF
from django.middleware.csrf import get_token
# from django.views.decorators.csrf import csrf_exempt

@login_required
def my_view(request):
    # Your view logic here
    return render(request, 'my_template.html')

def csrf_token_view(request):
    return JsonResponse({'csrfToken': get_token(request)})

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
        user = User.objects.create_user(username=username, email=email, password=password)

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
    # Ensure the request method is POST
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=400)

    # Parse the JSON request body
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    # Get username and password from the parsed data
    username = data.get('username')
    password = data.get('password')
    # Check if username and password are provided
    if not username or not password:
        return JsonResponse({'error': 'Username and password are required'}, status=400)

    # Authenticate the user
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        # Login the user
        login(request, user)
        response = JsonResponse({'message': 'Login successful', 'status': 'success'}, status=200)
        response.set_cookie('auth_token', 'user_token_here', httponly=True, secure=True)
        return response
    else:
        return JsonResponse({'error': 'Invalid username or password', 'status': 'error'}, status=401)
    
def logout_view(request):
    logout(request)
    response = JsonResponse({'message': 'Logout successful'})
    response.delete_cookie('auth_token')
    return response