from django.core.exceptions import ValidationError
from typing import List, Tuple, Any
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

"""
This model is used to represent a friendship between two users.

en este modelo se representa una amistad entre dos usuarios y se crea una relación de muchos a muchos

tenemos el estado de la solicitud de amistad, que puede ser pendiente, aceptada, denegada o bloqueada

se crea una relación de muchos a muchos con el modelo User de Django, que representa a los usuarios que pueden ser amigos

se crea un campo booleano para saber si un usuario está bloqueado o no

se crea un campo de fecha y hora para saber cuándo se creó la relación de amistad
"""
User: settings.AUTH_USER_MODEL = get_user_model()


class Friendship(models.Model):
    # Estado de la solicitud de amistad
    PENDING: str = "PENDING"
    ACCEPTED: str = "ACCEPTED"
    DENIED: str = "DENIED"
    BLOCKED: str = "BLOCKED"

    STATUS_CHOICES: List[Tuple[str, str]] = [
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (DENIED, "Denied"),
        (BLOCKED, "Blocked"),
    ]

    user = models.ForeignKey(
        User, related_name="user_friendships", on_delete=models.CASCADE
    )
    friend = models.ForeignKey(
        User, related_name="friend_user_friendships", on_delete=models.CASCADE
    )

    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=PENDING)

    is_blocked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """evita que un usuario sea amigo de sí mismo y verifica si la relación ya está bloqueada o si hay un bloqueo inverso"""

        unique_together: Tuple[str, str] = (
            "user",
            "friend",
        )

        indexes: List[models.Index] = [
            models.Index(fields=["user", "friend"]),
            models.Index(fields=["friend", "user"]),
        ]

    def __str__(self) -> str:
        return f"{self.user.username} -> {
            self.to_friend.username} [{self.status}]"

    def clean(self) -> None:
        """Evita que un usuario sea amigo de sí mismo"""
        # Verifica si la relación ya está bloqueada o si hay un bloqueo inverso
        if self.user == self.friend:
            raise ValidationError(
                "A user cannot send a friendship request to themselves."
            )
        elif self.is_blocked:
            raise ValidationError("You cannot interact with a blocked user.")
        elif Friendship.objects.filter(
            user=self.friend, friend=self.user, status=self.ACCEPTED
        ).exists():
            raise ValidationError(
                "This friendship already exists in the opposite direction and has been accepted."
            )

    def save(self, *args: list[str], **kwargs: dict[str, Any]) -> None:
        """Llama al método clean() antes de guardar"""
        self.clean()
        super(Friendship, self).save(*args, **kwargs)

    def block(self) -> None:
        """Bloquea a un usuario, terminando cualquier relación de amistad."""
        self.status = self.BLOCKED
        self.is_blocked = models.BooleanField(True)
        self.save()

    def unblock(self) -> None:
        """Desbloquea a un usuario, permitiendo futuras interacciones."""
        self.status = self.DENIED  # Resetea el estado de la relación
        self.is_blocked = models.BooleanField(False)
        self.save()
