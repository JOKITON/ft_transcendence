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
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, default="avatars/pepe.png")
    """ LO HA HECHO JOKIN? """
    """ profile = models.ImageField(upload_to="profile/", blank=True, null=True) """
    """ campo para la ruta del avatar """
    """ upload_to='avatars/': Esto especifica el directorio dentro de MEDIA_ROOT donde 
    se almacenarán las imágenes cargadas. En este caso, avatars/ es el subdirectorio 
    dentro de MEDIA_ROOT donde se guardarán las imágenes de los avatares. Si MEDIA_ROOT 
    está configurado como media/, entonces las imágenes se almacenarán en media/avatars/. """
    """ avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, max_length=5000, default='avatars/pepe.png') """
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
