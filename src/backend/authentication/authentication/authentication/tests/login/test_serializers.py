from rest_framework.test import APITestCase
from ...serializers import UserLoginSerializer


class UserSerializerTestCase(APITestCase):
    def setUp(self):
        # Configura los datos necesarios para las pruebas
        self.valid_data = {
            "username": "testuser",
            "password": "password123",
        }
        self.serializer = UserLoginSerializer(data=self.valid_data)

    def test_serializer_valid(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serializer_invalid(self):
        invalid_data = self.valid_data.copy()
        invalid_data["password"] = ""
        serializer = UserLoginSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
