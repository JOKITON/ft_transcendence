from UserModel.models import User
from django.db import models


class Room(models.Model):
    room = models.CharField(max_length=100, unique=True)
    online = models.ManyToManyField(to=User)
    create = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.create}  room name: {self.room}"


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    message = models.CharField(null=False)
    timestamp = models.DateTimeField(auto_now=True)


def __str__(self) -> str:
    return f"{self.timestamp}  {self.user}  {self.message}"
