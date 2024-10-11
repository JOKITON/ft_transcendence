# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views_get.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/30 22:18:38 by jaizpuru          #+#    #+#              #
#    Updated: 2024/10/11 17:45:50 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Player, PongGame
from .serializers import PongGameSerializer

class UserDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        print(request)
        # Fetch the player data for the current user
        try:
            player = Player.objects.get(id=pk or request.user.id)
        except Player.DoesNotExist:
            return Response(data={"message": "Player not found"}, status=status.HTTP_404_NOT_FOUND)
        
        player_data = {
            "id": player.id,
            "username": player.name,
            "wins": player.wins,
            "losses": player.losses,
            "avg_score": player.avg_score,
            "total_games": player.total_games,
            # Add other fields as necessary
        }
        print(player_data)
        return Response(data=player_data, status=status.HTTP_200_OK)

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
