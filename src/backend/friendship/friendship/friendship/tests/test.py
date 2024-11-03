from django.test import TestCase
from ..models import Friendship
from rest_framework.test import APIRequestFactory


"""
al final lo que tenemos es una referencia al id de los usuarios porque lo que hacemos
"""


class FriendshipTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = "invite"
        self.obj = Friendship.objects.create(user1="test1", user2="test2", status="P")

        self.assertEqual(self.obj.status, "P")

    def test_create_friendship(self):
        request = self.factory.post(
            self.url,
            data={
                "user1": "test1",
                "user2": "test2",
                "status": "P",
            },
            format="json",
        )
        response = self.view(request)
        self.assertEqual(Friendship.objects.count(), 1)
        self.assertEqual(Friendship.objects.get().user1, "test1")
        self.assertEqual(response.status_code, 201)
