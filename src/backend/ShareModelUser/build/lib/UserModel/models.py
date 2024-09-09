from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    nickname: models.CharField = models.CharField(max_length=50, blank=True, null=True)

    ip: models.CharField = models.GenericIPAddressField(
        blank=True, null=True, editable=False
    )

    last_login: models.DateTimeField = models.DateTimeField(
        auto_now=True, editable=False
    )

    last_request: models.DateTimeField = models.DateTimeField(
        auto_now=True, editable=False
    )

    last_update: models.DateTimeField = models.DateTimeField(
        auto_now=True, editable=False
    )

    created_at: models.DataField = models.DateTimeField(
        auto_now_add=True, editable=False
    )

    profile: models.ImagenField = models.ImageField(
        upload_to="profile/", blank=True, null=True
    )

    groups: models.ManyToManyField = models.ManyToManyField(
        Group,
        related_name="user_set",
        related_query_name="user",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )

    user_permissions: models.ManyToManyField = models.ManyToManyField(
        Permission,
        related_name="user_set",
        related_query_name="user",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    def __str__(self) -> str:
        return self.username
