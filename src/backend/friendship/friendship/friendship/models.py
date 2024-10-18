from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from typing import List, Tuple, Any
from django.db import models

User = get_user_model()

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

    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default=PENDING
    )

    # Cada campo maneja si uno de los usuarios bloqueó al otro
    is_blocked_user = models.BooleanField(default=False)  # Bloqueo hecho por `user`
    is_blocked_friend = models.BooleanField(default=False)  # Bloqueo hecho por `friend`

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    room = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together: Tuple[str, str] = ("user", "friend")
        indexes: List[models.Index] = [
            models.Index(fields=["user", "friend"]),
            models.Index(fields=["friend", "user"]),
        ]

    def __str__(self: Any) -> str:
        return f"{self.user.username} -> {self.friend.username} [{self.status}]"

    def clean(self: Any) -> None:
        if self.user == self.friend:
            raise ValidationError("A user cannot send a friendship request to themselves.")
        elif (
            User.objects.filter(pk=self.friend.pk).exists() is False
            or User.objects.filter(pk=self.user.pk).exists() is False
        ):
            raise ValidationError("The user does not exist.")
        elif Friendship.objects.filter(
            user=self.friend, friend=self.user, status=self.ACCEPTED
        ).exists():
            raise ValidationError("This friendship already exists in the opposite direction and has been accepted.")

    def save(self: Any, *args: Any, **kwargs: Any) -> None:
        self.clean()
        super(Friendship, self).save(*args, **kwargs)

    def block(self: Any, blocking_user: User) -> None:
        """Bloquea a un usuario, terminando cualquier relación de amistad."""
        if blocking_user == self.user:
            self.is_blocked_user = True
        elif blocking_user == self.friend:
            self.is_blocked_friend = True
        else:
            raise ValidationError("Invalid user for blocking.")
        
        self.status = self.BLOCKED
        self.save()

    def unblock(self: Any, unblocking_user: User) -> None:
        """Desbloquea a un usuario, permitiendo futuras interacciones."""
        if unblocking_user == self.user:
            self.is_blocked_user = False
        elif unblocking_user == self.friend:
            self.is_blocked_friend = False
        else:
            raise ValidationError("Invalid user for unblocking.")

        # Solo cambiar el estado a ACCEPTED si ambos usuarios están desbloqueados
        if not self.is_blocked_user and not self.is_blocked_friend:
            self.status = self.ACCEPTED
        
        self.save()