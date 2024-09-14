from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from typing import Tuple


class User(AbstractUser):
    Online: str = "Online"
    Offline: str = "Offline"
    Absent: str = "Absent"

    STATUS_CHOICES: list[Tuple[str, str]] = [
        (Online, "Online"),
        (Offline, "Offline"),
        (Absent, "Absent"),
    ]

    nickname = models.CharField(max_length=50, unique=True)
    ip = models.GenericIPAddressField(editable=True)
    ip_last_login = models.GenericIPAddressField(editable=True)
    last_login = models.DateTimeField(auto_now=True)
    last_request = models.DateTimeField(auto_now=True)
    last_update = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ImageField(upload_to="profile/", blank=True, null=True)
    status = models.CharField(
        max_length=7, choices=STATUS_CHOICES, default=Offline)

    groups = models.ManyToManyField(
        Group,
        related_name="user_set",
        related_query_name="user",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_set",
        related_query_name="user",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    def __str__(self):
        return self.username
