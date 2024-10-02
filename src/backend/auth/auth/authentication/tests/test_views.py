from django.urls import reverse
from ..views import RegisterUserView
from ..models import User  # Asegúrate de importar CustomUser
from rest_framework.test import APIRequestFactory
from django.test import TestCase


class UserCreateViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = RegisterUserView.as_view()
        self.url = reverse("register")

    def test_create_user(self):
        request = self.factory.post(
            self.url,
            data={
                "username": "testuser",
                "email": "ciclos@ciclos.com",
                "password": "testpassword",
            },
            format="json",
        )

        response = self.view(request)
        print("response is", response)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")
        self.assertEqual(response.status_code, 201)
