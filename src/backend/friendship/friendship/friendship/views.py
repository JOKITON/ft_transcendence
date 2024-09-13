from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from typing import Dict, Any
from .serializers import InviteFriendSerializer


class AllUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Dict[str, Any]) -> Response:
        users = get_user_model().objects.values(
            "username",
        )
        return Response(users, status=status.HTTP_200_OK)


class InviteFriendView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    """
    entonces tenemos que recibir el nombre del usuario que queremos invitar,
    tenemos al usuario que lo solicita y el usuario que va a ser invitado
    """

    def post(self, request: Dict[str, Any]) -> Response:
        serializer = InviteFriendSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": f"Invitacion enviada a {
                    serializer.data.get('friend')}"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "error al enviar la invitacion"},
            status=status.HTTP_400_BAD_REQUEST,
        )
