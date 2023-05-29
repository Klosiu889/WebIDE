from django.contrib.auth.models import User
from django.test import Client, TestCase, tag
from django.utils import timezone
from webIDE.models import Directory, File


class IndexTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test-user", password="test-password"
        )
        self.client = Client()
        self.client.login(username="test-user", password="test-password")

    def test_index(self):
        response = self.client.get("/webIDE/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")


class AddItemTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test-user", password="test-password"
        )
        self.client = Client()
        self.client.login(username="test-user", password="test-password")

        self.dir_home = Directory(
            path="test-user",
            name="test-user",
            creation_date=timezone.now(),
            owner=self.user,
            availability=True,
            availability_change_date=timezone.now(),
            change_date=timezone.now(),
            parent=None,
        )
        self.dir_home.save()

    def add_file_request(self, data, expected_response):
        database_initial_size = File.objects.count()
        response = self.client.post("/webIDE/add_item/", data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertJSONEqual(response.content, expected_response)
        if expected_response["status"] == "ok":
            self.assertTrue(
                File.objects.filter(path=expected_response["path"]).exists()
            )
        else:
            self.assertEqual(database_initial_size, File.objects.count())

    def add_directory_request(self, data, expected_response):
        database_initial_size = Directory.objects.count()
        response = self.client.post("/webIDE/add_item/", data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertJSONEqual(response.content, expected_response)
        if expected_response["status"] == "ok":
            self.assertTrue(
                Directory.objects.filter(path=expected_response["path"]).exists()
            )
        else:
            self.assertEqual(database_initial_size, Directory.objects.count())

    def test_add_file(self):
        data = {"name": "test-name", "parent": "test-user", "type": "file"}
        expected_response = {
            "status": "ok",
            "name": "test-name",
            "path": "test-user/test-name",
            "parent": "test-user",
            "content": "",
            "availability": True,
        }

        self.add_file_request(data, expected_response)

        data = {"name": "", "parent": "test-user", "type": "file"}
        expected_response = {"status": "error", "message": "Name cannot be empty"}

        self.add_file_request(data, expected_response)

        data = {"name": "test-name", "parent": "test-user", "type": "file"}
        expected_response = {"status": "error", "message": "File already exists"}

        self.add_file_request(data, expected_response)

    def test_add_directory(self):
        data = {"name": "test-name", "parent": "test-user", "type": "directory"}
        expected_response = {
            "status": "ok",
            "name": "test-name",
            "path": "test-user/test-name",
            "parent": "test-user",
            "content": "",
            "availability": True,
        }

        self.add_directory_request(data, expected_response)

        data = {"name": "", "parent": "test-user", "type": "directory"}
        expected_response = {"status": "error", "message": "Name cannot be empty"}

        self.add_directory_request(data, expected_response)

        data = {"name": "test-name", "parent": "test-user", "type": "directory"}
        expected_response = {"status": "error", "message": "Directory already exists"}

        self.add_directory_request(data, expected_response)


class DeleteItemTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test-user", password="test-password"
        )
        self.client = Client()
        self.client.login(username="test-user", password="test-password")

        self.dir_home = Directory(
            path="test-user",
            name="test-user",
            creation_date=timezone.now(),
            owner=self.user,
            availability=True,
            availability_change_date=timezone.now(),
            change_date=timezone.now(),
            parent=None,
        )
        self.dir_home.save()

        self.dir_test = Directory(
            path="test-user/test-dir",
            name="test-dir",
            creation_date=timezone.now(),
            owner=self.user,
            availability=True,
            availability_change_date=timezone.now(),
            change_date=timezone.now(),
            parent=self.dir_home,
        )
        self.dir_test.save()

        self.file_test = File(
            path="test-user/test-file",
            name="test-file",
            creation_date=timezone.now(),
            owner=self.user,
            availability=True,
            availability_change_date=timezone.now(),
            change_date=timezone.now(),
            parent=self.dir_home,
            content="test-content",
        )
        self.file_test.save()

    def delete_item_request(self, data, expected_response):
        response = self.client.post("/webIDE/delete_item/", data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertJSONEqual(response.content, expected_response)
        if expected_response["status"] == "ok":
            if data["type"] == "file":
                self.assertFalse(File.objects.get(path=data["path"]).availability)
            else:
                self.assertFalse(Directory.objects.get(path=data["path"]).availability)

    def test_delete_file(self):
        data = {"path": "test-user/test-file", "type": "file"}
        expected_response = {
            "status": "ok",
        }

        self.delete_item_request(data, expected_response)

        data = {"path": "", "type": "file"}
        expected_response = {"status": "error", "message": "Item was not selected"}

        self.delete_item_request(data, expected_response)

    def test_delete_directory(self):
        data = {"path": "test-user/test-dir", "type": "directory"}
        expected_response = {
            "status": "ok",
        }

        self.delete_item_request(data, expected_response)

        data = {"path": "", "type": "directory"}
        expected_response = {"status": "error", "message": "Item was not selected"}

        self.delete_item_request(data, expected_response)


class SaveFileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test-user", password="test-password"
        )
        self.client = Client()
        self.client.login(username="test-user", password="test-password")

        self.dir_home = Directory(
            path="test-user",
            name="test-user",
            creation_date=timezone.now(),
            owner=self.user,
            availability=True,
            availability_change_date=timezone.now(),
            change_date=timezone.now(),
            parent=None,
        )
        self.dir_home.save()

        self.file_test = File(
            path="test-user/test-file",
            name="test-file",
            creation_date=timezone.now(),
            owner=self.user,
            availability=True,
            availability_change_date=timezone.now(),
            change_date=timezone.now(),
            parent=self.dir_home,
            content="test-content",
        )
        self.file_test.save()

    def save_file_request(self, data, expected_response):
        response = self.client.post("/webIDE/save_file/", data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertJSONEqual(response.content, expected_response)
        if expected_response["status"] == "ok":
            self.assertEqual(
                File.objects.get(path=data["path"]).content, data["content"]
            )

    def test_save_file(self):
        data = {"path": "test-user/test-file", "content": "new-content"}
        expected_response = {"status": "ok", "content": "new-content"}

        self.save_file_request(data, expected_response)

        data = {"path": "", "content": "new-content"}
        expected_response = {"status": "error", "message": "File was not selected"}

        self.save_file_request(data, expected_response)


class DownloadFileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test-user", password="test-password"
        )
        self.client = Client()
        self.client.login(username="test-user", password="test-password")

        self.dir_home = Directory(
            path="test-user",
            name="test-user",
            creation_date=timezone.now(),
            owner=self.user,
            availability=True,
            availability_change_date=timezone.now(),
            change_date=timezone.now(),
            parent=None,
        )
        self.dir_home.save()

        self.file_test = File(
            path="test-user/test-file",
            name="test-file",
            creation_date=timezone.now(),
            owner=self.user,
            availability=True,
            availability_change_date=timezone.now(),
            change_date=timezone.now(),
            parent=self.dir_home,
            content="test-content",
        )
        self.file_test.save()

    def test_download_file(self):
        data = {"path": "test-user/test-file"}
        response = self.client.post("/webIDE/download_file/", data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertEqual(
            response["Content-Disposition"], "attachment; filename=test-file"
        )
        self.assertEqual(response.content, b"test-content")

        data = {"path": ""}
        expected_response = {"status": "error", "message": "File was not selected"}
        response = self.client.post("/webIDE/download_file/", data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertJSONEqual(response.content, expected_response)


@tag("compile")
class CompileFileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test-user", password="test-password"
        )
        self.client = Client()
        self.client.login(username="test-user", password="test-password")

        self.dir_home = Directory(
            path="test-user",
            name="test-user",
            creation_date=timezone.now(),
            owner=self.user,
            availability=True,
            availability_change_date=timezone.now(),
            change_date=timezone.now(),
            parent=None,
        )
        self.dir_home.save()

        self.file_test = File(
            path="test-user/test-file.c",
            name="test-file.c",
            creation_date=timezone.now(),
            owner=self.user,
            availability=True,
            availability_change_date=timezone.now(),
            change_date=timezone.now(),
            parent=self.dir_home,
            content="#include <stdio.h>\n\nint main() {\n\treturn 0;\n}",
        )
        self.file_test.save()

        self.file_test_empty = File(
            path="test-user/test-file-empty.c",
            name="test-file-empty.c",
            creation_date=timezone.now(),
            owner=self.user,
            availability=True,
            availability_change_date=timezone.now(),
            change_date=timezone.now(),
            parent=self.dir_home,
            content="",
        )
        self.file_test_empty.save()

        self.file_test_wrong_type = File(
            path="test-user/test-file-empty.wrong",
            name="test-file-empty.wrong",
            creation_date=timezone.now(),
            owner=self.user,
            availability=True,
            availability_change_date=timezone.now(),
            change_date=timezone.now(),
            parent=self.dir_home,
            content="",
        )
        self.file_test_wrong_type.save()

    def compile_file_request(self, data, expected_response):
        response = self.client.post("/webIDE/compile_file/", data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        if expected_response["status"] == "ok":
            expected_response["content"] = response.json()["content"]
        else:
            expected_response["error"] = response.json()["error"]

        self.assertJSONEqual(response.content, expected_response)
        if expected_response["status"] == "ok":
            self.assertTrue(
                File.objects.filter(path=data["file"][:-2] + ".asm").exists()
            )
            self.assertTrue(
                File.objects.get(path=data["file"][:-2] + ".asm").owner == self.user
            )
            self.assertTrue(
                File.objects.get(path=data["file"][:-2] + ".asm").parent
                == self.dir_home
            )
            self.assertTrue(
                File.objects.get(path=data["file"][:-2] + ".asm").content != ""
            )
            self.assertTrue(
                File.objects.get(path=data["file"][:-2] + ".asm").availability
            )

    def test_compile_file(self):
        data = {
            "file": "test-user/test-file.c",
            "standard": "",
            "optimisation": "",
            "processor": "",
            "dependant": "",
        }
        expected_response = {
            "status": "ok",
            "name": "test-file.asm",
            "path": "test-user/test-file.asm",
            "parent": "test-user",
            "availability": True,
            "content": "",
        }

        self.compile_file_request(data, expected_response)

        data = {
            "file": "test-user/test-file-empty.c",
            "standard": "",
            "optimisation": "",
            "processor": "",
            "dependant": "",
        }
        expected_response = {
            "status": "error",
            "message": "Compilation failed with error code: 1",
            "error": "",
        }

        self.compile_file_request(data, expected_response)

        data = {
            "file": "test-user/test-file-empty.wrong",
            "standard": "",
            "optimisation": "",
            "processor": "",
            "dependant": "",
        }
        expected_response = {
            "status": "error",
            "message": "Compilation failed with error code: 1",
            "error": "",
        }

        self.compile_file_request(data, expected_response)

        data = {
            "file": "",
            "standard": "",
            "optimisation": "",
            "processor": "",
            "dependant": "",
        }

        expected_response = {
            "status": "error",
            "message": "File was not selected",
            "error": "",
        }

        self.compile_file_request(data, expected_response)
