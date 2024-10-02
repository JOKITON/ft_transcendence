# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views_get.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/30 22:18:38 by jaizpuru          #+#    #+#              #
#    Updated: 2024/10/02 17:30:23 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import PongGame
from .serializers import PongGameSerializer

class TournamentListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Query all Tournament objects
        tournaments = PongGame.objects.all()

        # Use the serializer to serialize the tournament data
        serializer = PongGameSerializer(tournaments, many=True)

        # Return the serialized data
        return Response(data=serializer.data, status=status.HTTP_200_OK)
