from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from webIDE.models import Directory, File, Item


class ItemTestCase(TestCase):
    def test_abstract_class(self):
        with self.assertRaises(TypeError):
            item = Item()


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

    def validate_length_constraint(self, field, dir_path='root/test'):
        dir_test = Directory.objects.get(path=dir_path)
        max_length = Directory._meta.get_field(field).max_length
        setattr(dir_test, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError):
            dir_test.full_clean()

    def validate_not_nullable(self, field, dir_path='root/test'):
        dir_test = Directory.objects.get(path=dir_path)
        setattr(dir_test, field, None)
        with self.assertRaises(ValidationError):
            dir_test.full_clean()

    def test_fields_validation(self):
        user = User.objects.get(username='test_user')

        # Check max_length constraint
        length_constrained = [
            'path',
            'name',
            'description'
        ]

        for field in length_constrained:
            self.validate_length_constraint(field)

        # Check not nullable constraint
        not_nullable = [
            'path',
            'name',
            'creation_date',
            'owner',
            'availability',
            'availability_change_date',
            'change_date'
        ]

        for field in not_nullable:
            self.validate_not_nullable(field)

        # Check database relations
        dir_home = Directory.objects.get(path='root')
        dir_test = Directory.objects.get(path='root/test')

        self.assertEqual(dir_home, dir_test.parent)

        # Check default values
        dir_test = Directory(
            path='root/test2',
            name='test2',
            creation_date=self.date,
            owner=user,
            availability_change_date=self.date,
            change_date=self.date,
            parent=dir_home
        )

        self.assertEqual(dir_test.availability, True)


class FileTestCase(TestCase):
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
        file_test = File(
            path='root/test',
            name='test',
            description='test directory',
            creation_date=self.date,
            owner=user,
            availability=True,
            availability_change_date=self.date,
            change_date=self.date,
            parent=dir_home,
            content='test content'
        )
        dir_home.save()
        file_test.save()

    def test_create_directory(self):
        user = User.objects.get(username='test_user')
        dir_home = Directory.objects.get(path='root')
        file_test = File.objects.get(path='root/test')

        # Check file_test
        self.assertEqual(file_test.path, 'root/test')
        self.assertEqual(file_test.name, 'test')
        self.assertEqual(file_test.description, 'test directory')
        self.assertEqual(file_test.creation_date, self.date)
        self.assertEqual(file_test.owner, user)
        self.assertEqual(file_test.availability, True)
        self.assertEqual(file_test.availability_change_date, self.date)
        self.assertEqual(file_test.change_date, self.date)
        self.assertEqual(file_test.parent, dir_home)
        self.assertEqual(file_test.content, 'test content')

    def validate_length_constraint(self, field, file_path='root/test'):
        file_test = File.objects.get(path=file_path)
        max_length = Directory._meta.get_field(field).max_length
        setattr(file_test, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError):
            file_test.full_clean()

    def validate_not_nullable(self, field, file_path='root/test'):
        file_test = File.objects.get(path=file_path)
        setattr(file_test, field, None)
        with self.assertRaises(ValidationError):
            file_test.full_clean()

    def test_fields_validation(self):
        user = User.objects.get(username='test_user')

        # Check max_length constraint
        length_constrained = [
            'path',
            'name',
            'description'
        ]

        for field in length_constrained:
            self.validate_length_constraint(field)

        # Check not nullable constraint
        not_nullable = [
            'path',
            'name',
            'creation_date',
            'owner',
            'availability',
            'availability_change_date',
            'change_date'
        ]

        for field in not_nullable:
            self.validate_not_nullable(field)

        # Check database relations
        dir_home = Directory.objects.get(path='root')
        file_test = File.objects.get(path='root/test')

        self.assertEqual(dir_home, file_test.parent)

        # Check default values
        file_test = File(
            path='root/test2',
            name='test2',
            creation_date=self.date,
            owner=user,
            availability_change_date=self.date,
            change_date=self.date,
            parent=dir_home
        )

        self.assertEqual(file_test.availability, True)
