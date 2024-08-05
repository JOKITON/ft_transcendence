from django.test import TestCase
from ..models import User  # Asegúrate de importar tus modelos


class MyModelTestCase(TestCase):
    def setUp(self):
        self.obj = User.objects.create(
            username="test", email="ciclos@ciclos.com", password="12345678"
        )

    def test_model_str(self):
        self.assertEqual(str(self.obj), "test")

    def test_model_username(self):
        self.assertEqual(self.obj.username, "test")

    def test_model_email(self):
        self.assertEqual(self.obj.email, "ciclos@ciclos.com")

    def test_model_password(self):
        self.assertEqual(self.obj.password, "12345678")
