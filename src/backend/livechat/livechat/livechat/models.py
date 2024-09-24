from UserModel.models import User
from django.db import models


class Room(models.Model):
    room = models.CharField(unique=True)
    online = models.ManyToManyField(to=User, blank=True)
    create = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.create}  room name: {self.room}"


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    message = models.TextField(blank=False, null=False, max_length=500)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.timestamp}  {self.user}  {self.message}"
