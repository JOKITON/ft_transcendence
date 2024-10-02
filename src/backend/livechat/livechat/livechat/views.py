from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import RoomDeleteSerializer, RoomSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Request
from rest_framework.response import Response
from rest_framework import status
from typing import Dict, Any
from .models import Room


class CreateRoomView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = RoomSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            valid = serializer.save()
            if valid:
                response: Dict[str, Any] = {
                    "message": "Room created successfully",
                    "status": status.HTTP_201_CREATED,
                }
                return Response(response, status=status.HTTP_201_CREATED)

        return Response(
            {
                "message": "Room not created",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteRoomView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request) -> Response:
        room = RoomDeleteSerializer(data=request.data, context={"request": request})
        if room.is_valid():
            room.save()
            if room is not None:
                response: Dict[str, Any] = {
                    "result": "Room deleted successfully",
                    "status": status.HTTP_200_OK,
                }
                return Response(response, status=status.HTTP_200_OK)

        return Response(
            {
                "result": "Room not deleted",
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class ListRoomView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        rooms = Room.objects.all()
        return Response(rooms.data, status=status.HTTP_200_OK)
