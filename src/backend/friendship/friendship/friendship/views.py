from .serializers import (
    InviteFriendSerializer,
    InviteStatusSerializer,
    FriendshipDeleteSerializers,
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
                "status",
            )
            .exclude(id=request.user.id)
        )
        return Response(users, status=status.HTTP_200_OK)


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
        serializer = FriendshipDeleteSerializers(
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
        friendships = Friendship.objects.filter(
            models.Q(user=user) | models.Q(friend=user), status=Friendship.ACCEPTED
        )
        friends = [
            friendship.friend if friendship.user == user else friendship.user
            for friendship in friendships
        ]
        serializer = FriendSerializer(friends, many=True, context={"request": request})

        return Response({"friends": serializer.data}, status=status.HTTP_200_OK)


class BlockUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
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

