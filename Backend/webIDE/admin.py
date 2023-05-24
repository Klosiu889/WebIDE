from django.contrib import admin

from .models import Directory, File

admin.site.register(Directory)
admin.site.register(File)
