from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    login = models.CharField(max_length=200, primary_key=True)
    password = models.CharField(max_length=200)


class Item(models.Model):
    path = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    creation_date = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    availability = models.BooleanField(default=True)
    availability_change_date = models.DateTimeField()
    change_date = models.DateTimeField()

    class Meta:
        abstract = True


class Directory(Item):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)


class File(Item):
    parent = models.ForeignKey(Directory, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
