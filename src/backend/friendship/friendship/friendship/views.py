from .serializers import (
    InviteFriendSerializer,
    InviteStatusSerializer,
    DeleteFriendSerializer,
    FriendRequestSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.db.models.base import ModelBase
from rest_framework.views import APIView
from requests.sessions import Request
from rest_framework import status
from .models import Friendship
from typing import Type
from .serializers import FriendRequestSerializer
from .serializers import FriendSerializer
from django.db import models

User: Type[ModelBase] = get_user_model()


class AllUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        users = (
            get_user_model()
            .objects.values(
                "id",
                "username",
                "status",  # Assuming status is a field on your User model
            )
            .exclude(id=request.user.id)  # Exclude the current user
        )
        
        return Response(data=users, status=status.HTTP_200_OK)



class FriendsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        user = request.user
        friends = Friendship.objects.filter(user=user)
        if not friends:
            return Response(
                {"message": "no tienes amigos"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response({"friends": friends}, status=status.HTTP_200_OK)


class InviteFriendView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = InviteFriendSerializer(
            data=request.data, context={"request": request}
        )
        print("holaa")
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": f"Invitacion enviada a {
                        serializer.data.get('friend')}"
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "error al enviar la invitacion"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class InviteStatusView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        user = request.user
        friend = User.objects.get(username=request.data.get("friend"))

        try:
            friendship = Friendship.objects.get(user=user, friend=friend)
        except Friendship.DoesNotExist:
            return Response(
                {"message": "solicitud de amistad no encontrada"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = InviteStatusSerializer(
            friendship, data=request.data, context={"request": request}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "status friend update"}, status.HTTP_201_CREATED
            )
        return Response(
            {"message": "error al actualizar el estado de la invitacion"},
            status.HTTP_400_BAD_REQUEST,
        )


class DeleteFriendView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request) -> Response:
        serializer = DeleteFriendSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.delete(serializer.validated_data)
            return Response(
                {"message": "friend deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)


class PendingFriendRequestsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        pending_requests = Friendship.objects.filter(
            friend=user, status=Friendship.PENDING
        )

        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(
            {"pending_requests": serializer.data}, status=status.HTTP_200_OK
        )


class AcceptFriendRequestView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        request_id = request.data.get("request_id")

        if not request_id:
            return Response(
                {"error": "Request ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            friendship = Friendship.objects.get(
                id=request_id, friend=user, status=Friendship.PENDING
            )
            friendship.status = Friendship.ACCEPTED
            friendship.save()

            return Response(
                {"message": "Friend request accepted"}, status=status.HTTP_200_OK
            )
        except Friendship.DoesNotExist:
            return Response(
                {"error": "Friend request not found or already processed"},
                status=status.HTTP_404_NOT_FOUND,
            )


class RejectFriendRequestView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        request_id = request.data.get("request_id")

        if not request_id:
            return Response(
                {"error": "Request ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            friendship = Friendship.objects.get(
                id=request_id, friend=user, status=Friendship.PENDING
            )
            friendship.status = Friendship.DENIED
            friendship.save()

            return Response(
                {"message": "Friend request denied"}, status=status.HTTP_200_OK
            )
        except Friendship.DoesNotExist:
            return Response(
                {"error": "Friend request not found or already processed"},
                status=status.HTTP_404_NOT_FOUND,
            )


class GetFriendsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Filtrar amistades aceptadas o bloqueadas
        friendships = Friendship.objects.filter(
<<<<<<< HEAD
            models.Q(user=user) | models.Q(friend=user), status=Friendship.ACCEPTED
        )
        friends = [
            friendship.friend if friendship.user == user else friendship.user
            for friendship in friendships
        ]
        serializer = FriendSerializer(friends, many=True, context={"request": request})
=======
            models.Q(user=user) | models.Q(friend=user),
            models.Q(status=Friendship.ACCEPTED) | models.Q(status=Friendship.BLOCKED)
        )
>>>>>>> merge

        friends = []
        for friendship in friendships:
            # Determina quién es el amigo en función del usuario actual
            if friendship.user == user:
                friend = friendship.friend
                is_blocked_by_user = friendship.is_blocked_user
                is_blocked_by_friend = friendship.is_blocked_friend
            else:
                friend = friendship.user
                is_blocked_by_user = friendship.is_blocked_friend
                is_blocked_by_friend = friendship.is_blocked_user

            friends.append({
                "id": friend.id,
                "username": friend.username,
                "email": friend.email,
                "is_blocked_by_user": is_blocked_by_user,  # Si el usuario actual bloqueó al amigo
                "is_blocked_by_friend": is_blocked_by_friend  # Si el amigo bloqueó al usuario actual
            })

        return Response({"friends": friends}, status=status.HTTP_200_OK)
    
#class GetFriendsView(APIView):
 #   authentication_classes = [JWTAuthentication]
 #   permission_classes = [IsAuthenticated]

#    def get(self, request):
 #       user = request.user
  #      friendships = Friendship.objects.filter(
   #         models.Q(user=user) | models.Q(friend=user),
    #        status=Friendship.ACCEPTED
     #   )
      #  friends = [
       #     friendship.friend if friendship.user == user else friendship.user
        #    for friendship in friendships
       # #]
       # serializer = FriendSerializer( context={'request': request})
       # return Response({"friends": serializer.data}, status=status.HTTP_200_OK#)


class BlockUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
<<<<<<< HEAD
        blocked_user = User.objects.get(username=request.data.get("username"))

        if blocked_user == user:
            return Response(
                {"error": "You cannot block yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            friendship = Friendship.objects.get(user=user, friend=blocked_user)
            friendship.status = Friendship.BLOCKED
            friendship.save()

            return Response({"message": "User blocked"}, status=status.HTTP_200_OK)
        except Friendship.DoesNotExist:
            return Response(
                {"error": "Friendship not found"}, status=status.HTTP_404_NOT_FOUND
            )

=======
        friend_username = request.data.get("friend_username")

        if not friend_username:
            return Response(
                {"error": "Friend username is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            friend = User.objects.get(username=friend_username)
            # Buscar la amistad en ambas direcciones
            friendship = Friendship.objects.filter(
                models.Q(user=user, friend=friend) | models.Q(user=friend, friend=user)
            ).first()

            if not friendship:
                return Response(
                    {"error": "Friendship not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Bloquear al usuario (pasando el bloqueador)
            friendship.block(user)

            return Response(
                {"message": f"User {friend_username} has been blocked by {user.username}"},
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"error": "Friend not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class UnlockUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        friend_username = request.data.get("friend_username")

        if not friend_username:
            return Response(
                {"error": "Friend username is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            friend = User.objects.get(username=friend_username)
            # Buscar la amistad en ambas direcciones
            friendship = Friendship.objects.filter(
                models.Q(user=user, friend=friend) | models.Q(user=friend, friend=user)
            ).first()

            if not friendship:
                return Response(
                    {"error": "Friendship not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Desbloquear al usuario (pasando el desbloqueador)
            friendship.unblock(user)

            return Response(
                {"message": f"User {friend_username} has been unblocked by {user.username}"},
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"error": "Friend not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
>>>>>>> merge
