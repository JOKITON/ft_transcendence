from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Request
from rest_framework.response import Response
from rest_framework import status
from typing import Dict, Any
from ..models import Room
from rest_framework import test
from django.test import TestCase


class MyModelTestCase(TestCase):
    def setUp(self):
        self.obj = Room.objects.create(room_name="test", users=["admin"])

    def test_model_str(self):
        self.assertEqual(str(self.obj), "test")
