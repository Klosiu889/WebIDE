from datetime import datetime

from django.shortcuts import render
from .models import Directory, File
from django.http import JsonResponse


def delete_Item(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        item_type = request.POST.get('type')
        if item_type == 'directory':
            item = Directory.objects.get(id=item_id)
            item.availability = False
            item.availability_change_date = datetime.now()
            item.save()
        elif item_type == 'file':
            item = File.objects.get(id=item_id)
            item.availability = False
            item.availability_change_date = datetime.now()
            item.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def save_file(request):
    if request.method == 'POST':
        file_id = request.POST.get('id')
        file_content = request.POST.get('content')
        file = File.objects.get(id=file_id)
        file.file_content = file_content
        file.change_date = datetime.now()
        file.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def index(request):
    directories = Directory.objects.all()
    files = File.objects.all()
    directories_list = list(directories.values())
    files_list = list(files.values())
    data = {
        'directories': directories,
        'files': files,
        'directories_list': directories_list,
        'files_list': files_list,
    }

    return render(request, 'index.html', data)
