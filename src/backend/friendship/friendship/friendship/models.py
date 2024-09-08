from django.core.exceptions import ValidationError
from django.conf import settings
from typing import List, Literal, Tuple
from django.db import models

"""
This model is used to represent a friendship between two users.

en este modelo se representa una amistad entre dos usuarios y se crea una relación de muchos a muchos

tenemos el estado de la solicitud de amistad, que puede ser pendiente, aceptada, denegada o bloqueada

se crea una relación de muchos a muchos con el modelo User de Django, que representa a los usuarios que pueden ser amigos

se crea un campo booleano para saber si un usuario está bloqueado o no 

se crea un campo de fecha y hora para saber cuándo se creó la relación de amistad
"""


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

    from_friend: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="friend_set", on_delete=models.CASCADE
    )

    to_friend: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="to_friend_set", on_delete=models.CASCADE
    )

    status: str | models.CharField = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default=PENDING
    )

    is_blocked: models.BooleanField = models.BooleanField(default=False)

    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, editable=False
    )

    update_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        """evita que un usuario sea amigo de sí mismo y verifica si la relación ya está bloqueada o si hay un bloqueo inverso"""

        unique_together: tuple = (
            "from_friend",
            "to_friend",
        )
        indexes: List = [
            models.Index(fields=["from_friend", "to_friend"]),
            models.Index(fields=["to_friend", "from_friend"]),
        ]
        print(__doc__)

    def __str__(self) -> str:
        return (
            f"{self.from_friend.username} -> {self.to_friend.username} [{self.status}]"
        )

    def clean(self) -> None:
        """Evita que un usuario sea amigo de sí mismo"""
        if self.from_friend == self.to_friend:
            raise ValidationError(
                "A user cannot send a friendship request to themselves."
            )
        print(__doc__)
        # Verifica si la relación ya está bloqueada o si hay un bloqueo inverso
        if self.is_blocked:
            raise ValidationError("You cannot interact with a blocked user.")

        if Friendship.objects.filter(
            from_friend=self.to_friend, to_friend=self.from_friend, status=self.ACCEPTED
        ).exists():
            raise ValidationError(
                "This friendship already exists in the opposite direction and has been accepted."
            )

    def save(self, *args, **kwargs) -> None:
        """Llama al método clean() antes de guardar"""
        self.clean()
        super(Friendship, self).save(*args, **kwargs)
        print(__doc__)

    def block(self) -> None:
        """Bloquea a un usuario, terminando cualquier relación de amistad."""
        self.status = self.BLOCKED
        self.is_blocked = models.BooleanField(True)
        self.save()
        print(__doc__)

    def unblock(self) -> None:
        """Desbloquea a un usuario, permitiendo futuras interacciones."""
        self.status = self.DENIED  # Resetea el estado de la relación
        self.is_blocked = models.BooleanField(False)
        self.save()
        print(__doc__)


"""
no creo que use este modelo no se
class FriendshipNotification(models.Model):
    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    friendship: models.ForeignKey = models.ForeignKey(
        Friendship, on_delete=models.CASCADE
    )
    message: models.CharField = models.CharField(max_length=255)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    read: models.BooleanField= models.BooleanField(default=False)
"""
