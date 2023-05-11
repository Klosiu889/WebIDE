from datetime import datetime

from django.shortcuts import render
from .models import Directory, File
import subprocess


def render_website(request):
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


def add_file(request):
    if request.method == 'POST' and request.POST.get('name') != "":
        file_name = request.POST.get('name')
        file = None
        if request.POST.get('parent') != "":
            parent_id = int(request.POST.get('parent'))
            parent = Directory.objects.get(id=parent_id)
            file = File(name=file_name, creation_date=datetime.now(), availability=True,
                        availability_change_date=datetime.now(), change_date=datetime.now(), parent=parent)
        else:
            file = File(name=file_name, creation_date=datetime.now(), availability=True,
                        availability_change_date=datetime.now(), change_date=datetime.now())
        file.save()
    return render_website(request)


def add_directory(request):
    if request.method == 'POST' and request.POST.get('name') != "":
        directory_name = request.POST.get('name')
        directory = None
        if request.POST.get('parent') != "":
            parent_id = int(request.POST.get('parent'))
            parent = Directory.objects.get(id=parent_id)
            directory = Directory(name=directory_name, creation_date=datetime.now(), availability=True,
                                  availability_change_date=datetime.now(), change_date=datetime.now(), parent=parent)
        else:
            directory = Directory(name=directory_name, creation_date=datetime.now(), availability=True,
                                  availability_change_date=datetime.now(), change_date=datetime.now())
        directory.save()
    return render_website(request)


def delete_item(request):
    if request.method == 'POST' and request.POST.get('id') != "":
        item_id = int(request.POST.get('id'))
        item_type = request.POST.get('type')
        if item_type == 'directory':
            directory = Directory.objects.get(id=item_id)
            directory.availability = False
            directory.availability_change_date = datetime.now()
            directory.save()
        elif item_type == 'file':
            file = File.objects.get(id=item_id)
            file.availability = False
            file.availability_change_date = datetime.now()
            file.save()

    return render_website(request)


def save_file(request):
    if request.method == 'POST' and request.POST.get('id') != "":
        file_id = int(request.POST.get('id'))
        file_content = request.POST.get('content')
        file = File.objects.get(id=file_id)
        file.content = file_content
        file.change_date = datetime.now()
        file.save()

    return render_website(request)


def compile_file(request):
    if request.method == 'POST' and request.POST.get('id') != "":
        standard = request.POST.get('standard')
        optimizations = request.POST.get('optimization')
        processor = request.POST.get('processor')
        dependant = request.POST.get('dependant')
        file_id = int(request.POST.get('file'))
        file = File.objects.get(id=file_id)

        command = "sdcc"
        if standard != "":
            command += " --" + standard

        if processor != "":
            command += " -" + processor

        command += " " + file.name
        print(command)
        file_create = open(file.name, 'w')
        file_create.write(file.content)
        file_create.close()
        subprocess.run(command, shell=True)
        new_entry = File(name=file.name[:-2] + ".asm", creation_date=datetime.now(), availability=True, availability_change_date=datetime.now(), change_date=datetime.now(), parent=file.parent)
        new_entry.content = open(file.name[:-2] + ".asm", 'r').read()
        new_entry.save()
        subprocess.run("rm " + file.name[:-2] + "*", shell=True)


    return render_website(request)


def index(request):
    return render_website(request)
