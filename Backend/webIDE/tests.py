from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Directory, Item


class ItemTestCase(TestCase):
    def setUp(self):
        item = Item()
        self.assertEqual(TypeError, item.save())


class DirectoryTestCase(TestCase):
    date = timezone.now()

    def setUp(self):
        user = User.objects.create_user(username='test_user', password='12345')
        user.save()
        dir_home = Directory(
            path='root',
            name='root',
            description='root directory',
            creation_date=self.date,
            owner=user,
            availability=True,
            availability_change_date=self.date,
            change_date=self.date,
            parent=None
        )
        dir_test = Directory(
            path='root/test',
            name='test',
            description='test directory',
            creation_date=self.date,
            owner=user,
            availability=True,
            availability_change_date=self.date,
            change_date=self.date,
            parent=dir_home
        )
        dir_home.save()
        dir_test.save()

    def test_create_directory(self):
        user = User.objects.get(username='test_user')
        dir_home = Directory.objects.get(path='root')
        dir_test = Directory.objects.get(path='root/test')

        # Check dir_home
        self.assertEqual(dir_home.path, 'root')
        self.assertEqual(dir_home.name, 'root')
        self.assertEqual(dir_home.description, 'root directory')
        self.assertEqual(dir_home.creation_date, self.date)
        self.assertEqual(dir_home.owner, user)
        self.assertEqual(dir_home.availability, True)
        self.assertEqual(dir_home.availability_change_date, self.date)
        self.assertEqual(dir_home.change_date, self.date)
        self.assertEqual(dir_home.parent, None)

        # Check dir_test
        self.assertEqual(dir_test.path, 'root/test')
        self.assertEqual(dir_test.name, 'test')
        self.assertEqual(dir_test.description, 'test directory')
        self.assertEqual(dir_test.creation_date, self.date)
        self.assertEqual(dir_test.owner, user)
        self.assertEqual(dir_test.availability, True)
        self.assertEqual(dir_test.availability_change_date, self.date)
        self.assertEqual(dir_test.change_date, self.date)
        self.assertEqual(dir_test.parent, dir_home)
