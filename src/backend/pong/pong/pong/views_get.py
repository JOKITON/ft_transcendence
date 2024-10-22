# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views_get.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/30 22:18:38 by jaizpuru          #+#    #+#              #
#    Updated: 2024/10/22 19:20:47 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Player, PongGame
from django.db.models import Q
from .serializers import PongGameSerializer, LeaderBoardSerializer

class UserDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        print(request)
        # Fetch the player data for the current user
        try:
            player = Player.objects.get(id=pk or request.user.id)
        except PongGame.DoesNotExist:
            return Response(data={"message": "Player not found"}, status=status.HTTP_404_NOT_FOUND)
        
        player_data = {
            "id": player.id,
            "username": player.name,
            "wins": player.wins,
            "losses": player.losses,
            "avg_score": player.avg_score,
            "total_games": player.total_games,
            "time_played": player.time_played,
            "hits": player.hits,
            # Add other fields as necessary
        }
        print(player_data)
        return Response(data=player_data, status=status.HTTP_200_OK)
    
class PongGameDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk=None):
        print(request)
        # Fetch the player data for the current user
        try:
            game = PongGame.objects.get((Q(player1_id=pk) | Q(player2_id=pk)) & Q(status='P'))
        except PongGame.DoesNotExist:
            return Response(data={"message": "Game not found"}, status=status.HTTP_200_OK)
        
        game_data = {
            "id": game.id,
            "status": game.status,
            "tournament_type": game.tournament_type,
            "player_ids": game.player_ids,
            "player_names": game.player_names,
            "player_scores": game.player_scores,
            "player_hits": game.player_hits,
            "time_played": game.time_played,
            # Add other fields as necessary
        }
        print(game_data)
        return Response({"data": game_data}, status=status.HTTP_200_OK)

class LeaderBoardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Query all Player objects
        players = Player.objects.all().order_by('-wins')

        # Use the serializer to serialize the player data
        serializer = LeaderBoardSerializer(players, many=True)

        # Return the serialized data
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

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
