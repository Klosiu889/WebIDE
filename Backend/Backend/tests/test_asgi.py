import os

from django.core.asgi import get_asgi_application
from django.test import TestCase


class ASGITestCase(TestCase):
    def test_asgi_application(self):
        application = get_asgi_application()
        self.assertIsNotNone(application)

    def test_django_settings_module(self):
        self.assertEqual(os.environ.get("DJANGO_SETTINGS_MODULE"), "Backend.settings")
