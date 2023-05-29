from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_item/", views.add_item, name="add_directory"),
    path("delete_item/", views.delete_item, name="delete_item"),
    path("save_file/", views.save_file, name="save_file"),
    path("compile_file/", views.compile_file, name="compile_file"),
    path("download_file/", views.download_file, name="download_file"),
]
