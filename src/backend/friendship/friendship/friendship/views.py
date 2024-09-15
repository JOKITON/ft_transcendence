from .serializers import (
    InviteFriendSerializer,
    InviteStatusSerializer,
    DeleteFriendSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from requests.sessions import Request
from rest_framework import status


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


class InviteFriendView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = InviteFriendSerializer(
            data=request.data, context={"request": request}
        )
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
        serializer = InviteStatusSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.status = serializer.data.get("status")
            serializer.save()
            return Response(
                {"message": "status friend update"}, status.HTTP_201_CREATED
            )
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)


class DeleteFriendView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request) -> Response:
        serializer = DeleteFriendSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.delete()
            return Response(
                {"message": "friend deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)
