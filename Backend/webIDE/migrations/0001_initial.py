# Generated by Django 4.2 on 2023-05-06 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('creation_date', models.DateTimeField()),
                ('availability', models.BooleanField(default=True)),
                ('availability_change_date', models.DateTimeField()),
                ('change_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('login', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('creation_date', models.DateTimeField()),
                ('availability', models.BooleanField(default=True)),
                ('availability_change_date', models.DateTimeField()),
                ('change_date', models.DateTimeField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webIDE.user')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webIDE.directory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='directory',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webIDE.user'),
        ),
        migrations.AddField(
            model_name='directory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webIDE.directory'),
        ),
    ]
