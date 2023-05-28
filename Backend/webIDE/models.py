from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    path = models.CharField(max_length=1000, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    creation_date = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    availability = models.BooleanField(default=True)
    availability_change_date = models.DateTimeField()
    change_date = models.DateTimeField()

    class Meta:
        abstract = True


class Directory(Item):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)


class File(Item):
    parent = models.ForeignKey(Directory, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(default="", blank=True, null=True)
