from requests.sessions import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from typing import Dict
from .models import Round

User = get_user_model()

class TournamentAI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        model = Round(data=request.data)
        valid = model.save()
        if valid:
            response: Dict[str, Any] = {
                "message": "Pong game saved successfully",
                "status": status.HTTP_201_CREATED,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(
            {
                "message": "Pong game not saved",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class Tournament2P(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        model = Round(data=request.data)
        valid = model.save()
        if valid:
            response: Dict[str, Any] = {
                "message": "Pong game saved successfully",
                "status": status.HTTP_201_CREATED,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(
            {
                "message": "Pong game not saved",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class Tournament8P(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        return Response(status=status.HTTP_200_OK)
