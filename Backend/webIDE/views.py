import subprocess
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

from .models import Directory, File


def render_website(request):
    directories = Directory.objects.filter(owner=request.user)
    files = File.objects.filter(owner=request.user)
    directories_list = list(directories.values())
    files_list = list(files.values())
    data = {
        'directories': directories,
        'files': files,
        'directories_list': directories_list,
        'files_list': files_list,
    }
    return render(request, 'index.html', data)


def add_file(request):
    if request.method == 'POST' and request.POST.get('name') != "":
        file_name = request.POST.get('name')
        if request.POST.get('parent') != "":
            parent_path = request.POST.get('parent')
            parent = Directory.objects.get(path=parent_path)
            new_path = parent.path + '/' + file_name
            file = File(path=new_path, name=file_name,
                        creation_date=datetime.now(),
                        owner=request.user,
                        availability=True,
                        availability_change_date=datetime.now(),
                        change_date=datetime.now(),
                        parent=parent)
        else:
            file = File(path=request.user.username + "/" + file_name,
                        name=file_name,
                        creation_date=datetime.now(),
                        owner=request.user,
                        availability=True,
                        availability_change_date=datetime.now(),
                        change_date=datetime.now())
        file.save()
    return render_website(request)


def add_directory(request):
    if request.method == 'POST' and request.POST.get('name') != "":
        directory_name = request.POST.get('name')
        if request.POST.get('parent') != "":
            parent_path = request.POST.get('parent')
            parent = Directory.objects.get(path=parent_path)
            new_path = parent.path + '/' + directory_name
            directory = Directory(path=new_path, name=directory_name,
                                  creation_date=datetime.now(),
                                  owner=request.user,
                                  availability=True,
                                  availability_change_date=datetime.now(),
                                  change_date=datetime.now(),
                                  parent=parent)
        else:
            directory = Directory(path=request.user.username + "/" + directory_name,
                                  name=directory_name,
                                  creation_date=datetime.now(),
                                  owner=request.user,
                                  availability=True,
                                  availability_change_date=datetime.now(),
                                  change_date=datetime.now())
        directory.save()
    return render_website(request)


def delete_item(request):
    if request.method == 'POST' and request.POST.get('path') != "":
        item_path = request.POST.get('path')
        item_type = request.POST.get('type')
        if item_type == 'directory':
            directory = Directory.objects.get(path=item_path)
            directory.availability = False
            directory.availability_change_date = datetime.now()
            directory.save()
        elif item_type == 'file':
            file = File.objects.get(path=item_path)
            file.availability = False
            file.availability_change_date = datetime.now()
            file.save()

    return render_website(request)


def save_file(request):
    if request.method == 'POST' and request.POST.get('path') != "":
        file_path = request.POST.get('path')
        file_content = request.POST.get('content')
        file = File.objects.get(path=file_path)
        file.content = file_content
        file.change_date = datetime.now()
        file.save()

    return render_website(request)


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
        print(command)
        subprocess.run("mkdir compile", shell=True)
        file_create = open("compile/" + file.name, 'w')
        file_create.write(file.content)
        file_create.close()
        result = subprocess.run("cd compile && " + command, shell=True)

        if result.returncode != 0:
            subprocess.run("rm -rf compile", shell=True)
            return JsonResponse({'success': False})

        new_file_name = file.name[:-2] + ".asm"
        new_file_path = file.path[:-len(file.name)] + new_file_name
        print(file.path + "\n" + new_file_name + "\n" + new_file_path)
        new_entry = File(path=new_file_path, name=new_file_name, creation_date=datetime.now(), availability=True,
                         availability_change_date=datetime.now(), change_date=datetime.now(), parent=file.parent)
        new_entry.content = open("compile/" + file.name[:-2] + ".asm", 'r').read()
        new_entry.save()
        subprocess.run("rm -rf compile", shell=True)

    return JsonResponse({'success': True})


def index(request):
    return render_website(request)
