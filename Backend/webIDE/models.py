from django.db import models


class Directory(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    creation_date = models.DateTimeField('date created')
    owner = models.CharField(max_length=200)
    availability = models.BooleanField(default=True)
    availability_change_date = models.DateTimeField('date availability changed')
    change_date = models.DateTimeField('date changed')


class File(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, null=True)
    creation_date = models.DateTimeField('date created')
    owner = models.CharField(max_length=200)
    availability = models.BooleanField(default=True)
    availability_change_date = models.DateTimeField('date availability changed')
    change_date = models.DateTimeField('date changed')


class User(models.Model):
    name = models.CharField(max_length=200)
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
