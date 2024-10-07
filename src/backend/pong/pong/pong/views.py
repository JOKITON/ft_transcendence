# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/17 18:36:34 by jaizpuru          #+#    #+#              #
#    Updated: 2024/10/05 12:31:10 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from requests.sessions import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PongGameSerializer, Tournament8PSerializer

User = get_user_model()

class TournamentAIView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWT for authentication
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def post(self, request: Request) -> Response:
        serializer = PongGameSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # Save the tournament instance
            response = {
                "message": "Tournament game saved successfully",
                "status": status.HTTP_201_CREATED,
                "data": serializer.data,  # Return the serialized data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(
            {
                "message": "Tournament game not saved",
                "errors": serializer.errors,  # Return validation errors
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class Tournament2PView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWT for authentication
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def post(self, request: Request) -> Response:
        serializer = PongGameSerializer(data=request.data, context={"request": request})
        # serializer.create_players(validated_data=request.data)

        if serializer.is_valid():
            serializer.save()  # Save the tournament instance
            response = {
                "message": "Tournament game saved successfully",
                "status": status.HTTP_201_CREATED,
                "data": serializer.data,  # Return the serialized data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(
            {
                "message": "Tournament game not saved",
                "errors": serializer.errors,  # Return validation errors
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

class Tournament8P(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWT for authentication
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def post(self, request: Request) -> Response:
        serializer = Tournament8PSerializer(data=request.data)

        if serializer.is_valid():
            tournament = serializer.save()  # Save the tournament instance
            response = {
                "message": "Tournament game saved successfully",
                "status": status.HTTP_201_CREATED,
                "tournament_id": tournament.id,  # Return the serialized data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(
            {
                "message": "Tournament game not saved",
                "errors": serializer.errors,  # Return validation errors
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )