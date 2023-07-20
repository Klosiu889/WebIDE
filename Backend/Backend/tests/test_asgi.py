import os

from django.core.asgi import get_asgi_application
from django.test import TestCase

from Backend import asgi


class ASGITestCase(TestCase):
    def test_asgi_application(self):
        application = get_asgi_application()
        self.assertIsNotNone(application)

    def test_django_settings_module(self):
        django_settings_module = os.environ.get("DJANGO_SETTINGS_MODULE")
        self.assertEqual(django_settings_module, "Backend.settings")
