from django.shortcuts import render
from .models import Directory, File


def index(request):
    directories = Directory.objects.all()
    files = File.objects.all()
    data = {
        'directories': directories,
        'files': files,
    }
    return render(request, 'index.html', data)