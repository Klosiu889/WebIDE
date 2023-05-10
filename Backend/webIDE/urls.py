from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete_Item/', views.delete_Item, name='delete_Item'),
    path('save_file/', views.save_file, name='save_file'),
]
