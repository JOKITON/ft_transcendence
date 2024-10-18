from django.db import models


class Room(models.Model):
    room = models.CharField(max_length=100, unique=True)
    create = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.create}  room name: {self.room}"


class Message(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="messages")
    user = models.CharField(max_length=100)
    message = models.TextField()
    index = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.user}: {self.message}"
