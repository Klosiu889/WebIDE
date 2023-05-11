from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_file/', views.add_file, name='add_file'),
    path('add_directory/', views.add_directory, name='add_directory'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('save_file/', views.save_file, name='save_file'),
    path('compile_file/', views.compile_file, name='compile_file'),
]
