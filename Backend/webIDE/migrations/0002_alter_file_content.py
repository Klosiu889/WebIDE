# Generated by Django 4.2.1 on 2023-05-28 11:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('webIDE', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='content',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]