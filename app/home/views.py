from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import RegisterForm
from django.views.decorators.csrf import requires_csrf_token

def index(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Registration successful'}, status=200)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'index.html')
