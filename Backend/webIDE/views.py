import subprocess

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .forms import AddFileForm, AddDirectoryForm, DeleteItemForm, SaveFileForm
from .models import Directory, File


def render_website(request):
    directories_db = Directory.objects.filter(owner=request.user)
    files_db = File.objects.filter(owner=request.user)

    directories = []
    files = []
    for directory in directories_db:
        directories.append({
            'path': directory.path,
            'name': directory.name,
            'parent': directory.parent.path if directory.parent else "",
            'availability': directory.availability,
        })

    for file in files_db:
        files.append({
            'path': file.path,
            'name': file.name,
            'parent': file.parent.path if file.parent else "",
            'content': file.content if file.content else '',
            'availability': file.availability,
        })

    home_path = request.user.username
    if Directory.objects.filter(path=home_path).exists():
        home_db = Directory.objects.get(path=home_path)
    else:
        home_db = Directory(path=home_path,
                            name=request.user.username,
                            creation_date=timezone.now(),
                            owner=request.user,
                            availability=True,
                            availability_change_date=timezone.now(),
                            change_date=timezone.now(),
                            parent=None,
                            description="Home directory"
                            )
        home_db.save()

    home = {
        'path': home_db.path,
        'name': home_db.name,
    }

    data = {
        'home': home,
        'directories': directories,
        'files': files,
        'form_add_file': AddFileForm(),
        'form_add_dir': AddDirectoryForm(),
        'form_delete_item': DeleteItemForm(),
        'form_save_file': SaveFileForm(),
    }
    return render(request, 'index.html', data)


def add_item(request):
    if request.method == 'POST' and request.POST.get('name') != "":
        item_name = request.POST.get('name')
        parent_path = request.POST.get('parent')
        parent = Directory.objects.get(path=parent_path)
        item_path = parent_path + '/' + item_name
        item_type = request.POST.get('type')

        if item_type == 'file':
            if File.objects.filter(path=item_path).exists() and File.objects.get(path=item_path).availability:
                return JsonResponse({'status': 'error', 'message': 'File already exists'})
            item = File(path=item_path,
                        name=item_name,
                        creation_date=timezone.now(),
                        owner=request.user,
                        availability=True,
                        availability_change_date=timezone.now(),
                        change_date=timezone.now(),
                        parent=parent)
        else:
            if Directory.objects.filter(path=item_path).exists() and Directory.objects.get(path=item_path).availability:
                return JsonResponse({'status': 'error', 'message': 'Directory already exists'})
            item = Directory(path=item_path,
                             name=item_name,
                             creation_date=timezone.now(),
                             owner=request.user,
                             availability=True,
                             availability_change_date=timezone.now(),
                             change_date=timezone.now(),
                             parent=parent)
        item.save()
        return JsonResponse({
            'status': 'ok',
            'name': item.name,
            'path': item.path,
            'parent': item.parent.path,
            'content': "",
            'availability': True,
        })
    else:
        return JsonResponse({'status': 'error'})


def delete_item(request):
    if request.method == 'POST' and request.POST.get('path') != "":
        item_path = request.POST.get('path')
        item_type = request.POST.get('type')
        if item_type == 'directory':
            directory = Directory.objects.get(path=item_path)
            directory.availability = False
            directory.availability_change_date = timezone.now()
            directory.save()
        elif item_type == 'file':
            file = File.objects.get(path=item_path)
            file.availability = False
            file.availability_change_date = timezone.now()
            file.save()

        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Deleting failed'})


def save_file(request):
    if request.method == 'POST' and request.POST.get('path') != "":
        file_path = request.POST.get('path')
        file_content = request.POST.get('content')
        file = File.objects.get(path=file_path)
        file.content = file_content
        file.change_date = timezone.now()
        file.save()

        return JsonResponse({'status': 'ok', 'content': file_content})
    else:
        return JsonResponse({'status': 'error', 'message': 'Saving failed.'})


def compile_file(request):
    if request.method == 'POST' and request.POST.get('file') != "":
        standard = request.POST.get('standard')
        optimisations = request.POST.get('optimisation')
        optimisations_split = optimisations.split(' ')
        processor = request.POST.get('processor')
        dependant = request.POST.get('dependant')
        file_path = request.POST.get('file')
        file = File.objects.get(path=file_path)

        command = "sdcc"
        if standard != "":
            command += " --" + standard

        if processor != "":
            command += " -" + processor

        for optimisation in optimisations_split:
            if optimisation != "":
                command += " --" + optimisation

        if dependant != "":
            command += " --" + dependant

        command += " " + file.name

        subprocess.run("mkdir compile", shell=True)
        file_create = open("compile/" + file.name, 'w')
        file_create.write(file.content)
        file_create.close()
        result = subprocess.run("cd compile && " + command + " 2> error.err", shell=True)

        if result.returncode != 0:
            error = open("compile/error.err", 'r').read()
            subprocess.run("rm -rf compile", shell=True)
            return JsonResponse({
                'status': 'error',
                'message': 'Compilation failed with error code: ' + str(result.returncode),
                'error': 'Error message:\n' + error
            })

        new_file_name = file.name[:-2] + ".asm"
        new_file_path = file.path[:-len(file.name)] + new_file_name

        new_entry = File(
            path=new_file_path,
            name=new_file_name,
            creation_date=timezone.now(),
            owner=request.user,
            availability=True,
            availability_change_date=timezone.now(),
            change_date=timezone.now(),
            parent=file.parent)

        new_entry.content = open("compile/" + file.name[:-2] + ".asm", 'r').read()
        new_entry.save()
        subprocess.run("rm -rf compile", shell=True)

        return JsonResponse({
            'status': 'ok',
            'name': new_entry.name,
            'path': new_entry.path,
            'parent': new_entry.parent.path,
            'availability': True,
            'content': new_entry.content
        })
    else:
        return JsonResponse({'status': 'error', 'message': 'File was not selected.'})


def index(request):
    return render_website(request)
