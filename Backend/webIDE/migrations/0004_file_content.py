# Generated by Django 4.2 on 2023-05-09 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webIDE', '0003_alter_directory_name_alter_file_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
