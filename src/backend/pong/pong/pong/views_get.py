# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    views_get.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaizpuru <jaizpuru@student.42urduliz.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/09/30 22:18:38 by jaizpuru          #+#    #+#              #
#    Updated: 2024/10/24 17:44:59 by jaizpuru         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Player, PongGame, Tournament4P
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

class AnyPongGameDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_tournament(self, pk=None, tournament_type=None):
        # Fetch the player data for the current user
        try:
            tournament = Tournament4P.objects.get((Q(player_ids__contains=[pk])) & Q(tournament_type=tournament_type, status='P'))
        except Tournament4P.DoesNotExist:
            return Response(data={"message": "Game not found"}, status=status.HTTP_200_OK)
        
        tournament_data = {
            "id": tournament.id,
            "status": tournament.status,
            "tournament_type": tournament.tournament_type,
            "player_ids": tournament.player_ids,
            "player_names": tournament.player_names,
            "player_scores": tournament.player_scores,
            "player_hits": tournament.player_hits,
            "time_played": tournament.time_played,
            # Add other fields as necessary
        }
        print(tournament_data)
        return Response({"data": tournament_data}, status=status.HTTP_200_OK)


    def get(self, request, pk=None, tournament_type=None):
        print(request)
        # Fetch the player data for the current user
        if (tournament_type == '4P' or tournament_type == '8P'):
            return self.get_tournament(pk, tournament_type)
        try:
            game = PongGame.objects.get((Q(player1_id=pk) | Q(player2_id=pk)) & Q(tournament_type=tournament_type, status='P'))
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
        if not players:
            return Response(data={"message": "No players found"}, status=status.HTTP_404_NOT_FOUND)

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
