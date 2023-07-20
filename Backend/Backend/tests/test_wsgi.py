import os

from django.core.wsgi import get_wsgi_application
from django.test import TestCase

from Backend import wsgi


class WSGITestCase(TestCase):
    def test_asgi_application(self):
        application = get_wsgi_application()
        self.assertIsNotNone(application)

    def test_django_settings_module(self):
        self.assertEqual(os.environ.get("DJANGO_SETTINGS_MODULE"), "Backend.settings")
