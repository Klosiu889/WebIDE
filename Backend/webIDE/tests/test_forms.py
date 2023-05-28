from django.test import TestCase
from webIDE.forms import (
    AddDirectoryForm,
    AddFileForm,
    CompileFileForm,
    DeleteItemForm,
    SaveFileForm,
)
from webIDE.models import File, Item


class AddFileFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {'name': 'test_file', 'parent': 'root', 'type': 'file'}
        form = AddFileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'name': '', 'parent': 'root', 'type': 'file'}
        form = AddFileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'name': 'test_file', 'parent': '', 'type': 'file'}
        form = AddFileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'name': 'test_file', 'parent': 'root', 'type': ''}
        form = AddFileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_hidden_fields(self):
        form_data = {'name': 'test_file', 'parent': 'root', 'type': 'file'}
        form = AddFileForm(data=form_data)

        self.assertFalse(form.fields['name'].widget.is_hidden)
        self.assertTrue(form.fields['parent'].widget.is_hidden)
        self.assertTrue(form.fields['type'].widget.is_hidden)

    def test_length_constraint(self):
        max_length = Item._meta.get_field('name').max_length
        form_data = {'name': 'a' * (max_length + 1), 'parent': 'root', 'type': 'file'}
        form = AddFileForm(data=form_data)
        self.assertFalse(form.is_valid())

        max_length = Item._meta.get_field('path').max_length
        form_data = {'name': 'test_file', 'parent': 'a' * (max_length + 1), 'type': 'file'}
        form = AddFileForm(data=form_data)
        self.assertFalse(form.is_valid())


class AddDirectoryFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {'name': 'test_file', 'parent': 'root', 'type': 'file'}
        form = AddDirectoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'name': '', 'parent': 'root', 'type': 'file'}
        form = AddDirectoryForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'name': 'test_file', 'parent': '', 'type': 'file'}
        form = AddDirectoryForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'name': 'test_file', 'parent': 'root', 'type': ''}
        form = AddDirectoryForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_hidden_fields(self):
        form_data = {'name': 'test_file', 'parent': 'root', 'type': 'file'}
        form = AddDirectoryForm(data=form_data)

        self.assertFalse(form.fields['name'].widget.is_hidden)
        self.assertTrue(form.fields['parent'].widget.is_hidden)
        self.assertTrue(form.fields['type'].widget.is_hidden)

    def test_length_constraint(self):
        max_length = Item._meta.get_field('name').max_length
        form_data = {'name': 'a' * (max_length + 1), 'parent': 'root', 'type': 'file'}
        form = AddDirectoryForm(data=form_data)
        self.assertFalse(form.is_valid())

        max_length = Item._meta.get_field('path').max_length
        form_data = {'name': 'test_file', 'parent': 'a' * (max_length + 1), 'type': 'file'}
        form = AddDirectoryForm(data=form_data)
        self.assertFalse(form.is_valid())


class DeleteItemFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {'path': 'root/test_file', 'type': 'file'}
        form = DeleteItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'path': '', 'type': 'file'}
        form = DeleteItemForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'path': 'root/test_file', 'type': ''}
        form = DeleteItemForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_hidden_fields(self):
        form_data = {'path': 'root/test_file', 'type': 'file'}
        form = DeleteItemForm(data=form_data)

        self.assertTrue(form.fields['path'].widget.is_hidden)
        self.assertTrue(form.fields['type'].widget.is_hidden)

    def test_length_constraint(self):
        max_length = Item._meta.get_field('path').max_length
        form_data = {'path': 'a' * (max_length + 1), 'type': 'file'}
        form = DeleteItemForm(data=form_data)
        self.assertFalse(form.is_valid())


class SaveFileFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {'path': 'root/test_file', 'content': 'test content'}
        form = SaveFileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'path': '', 'content': 'test content'}
        form = SaveFileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'path': 'root/test_file', 'content': ''}
        form = SaveFileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_hidden_fields(self):
        form_data = {'path': 'root/test_file', 'content': 'test content'}
        form = SaveFileForm(data=form_data)

        self.assertTrue(form.fields['path'].widget.is_hidden)
        self.assertTrue(form.fields['content'].widget.is_hidden)

    def test_length_constraint(self):
        max_length = File._meta.get_field('path').max_length
        form_data = {'path': 'a' * (max_length + 1), 'content': 'test content'}
        form = SaveFileForm(data=form_data)
        self.assertFalse(form.is_valid())


class CompileFileFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {
            'file': 'root/test_file',
            'standard': 'test-standard',
            'optimisation': 'test-opt1 test-opt2',
            'processor': 'test-processor',
            'dependant': 'test-dependant'
        }
        form = CompileFileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'file': '',
            'standard': 'test-standard',
            'optimisation': 'test-opt1 test-opt2',
            'processor': 'test-processor',
            'dependant': 'test-dependant'
        }
        form = CompileFileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            'file': 'root/test_file',
            'standard': '',
            'optimisation': 'test-opt1 test-opt2',
            'processor': 'test-processor',
            'dependant': 'test-dependant'
        }
        form = CompileFileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            'file': 'root/test_file',
            'standard': 'test-standard',
            'optimisation': '',
            'processor': 'test-processor',
            'dependant': 'test-dependant'
        }
        form = CompileFileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            'file': 'root/test_file',
            'standard': 'test-standard',
            'optimisation': 'test-opt1 test-opt2',
            'processor': '',
            'dependant': 'test-dependant'
        }
        form = CompileFileForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            'file': 'root/test_file',
            'standard': 'test-standard',
            'optimisation': 'test-opt1 test-opt2',
            'processor': 'test-processor',
            'dependant': ''
        }
        form = CompileFileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_hidden_fields(self):
        form_data = {
            'file': 'root/test_file',
            'standard': 'test-standard',
            'optimisation': 'test-opt1 test-opt2',
            'processor': 'test-processor',
            'dependant': 'test-dependant'
        }
        form = CompileFileForm(data=form_data)

        self.assertTrue(form.fields['file'].widget.is_hidden)
        self.assertTrue(form.fields['standard'].widget.is_hidden)
        self.assertTrue(form.fields['optimisation'].widget.is_hidden)
        self.assertTrue(form.fields['processor'].widget.is_hidden)
        self.assertTrue(form.fields['dependant'].widget.is_hidden)

    def test_length_constraint(self):
        max_length = File._meta.get_field('path').max_length
        form_data = {
            'file': 'a' * (max_length + 1),
            'standard': 'test-standard',
            'optimisation': 'test-opt1 test-opt2',
            'processor': 'test-processor',
            'dependant': 'test-dependant'
        }
        form = CompileFileForm(data=form_data)
        self.assertFalse(form.is_valid())
