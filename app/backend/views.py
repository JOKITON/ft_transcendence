from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

