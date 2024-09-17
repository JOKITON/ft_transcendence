from rest_framework import serializers
from .models import Tournament, Tournament8P
from .models import Player, FinalRound, SemiFinal, Tournament8P

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['winner', 'player1', 'player2', 'score_player1', 'score_player2', 'tournament_type']


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['name', 'score', 'position']

class FinalRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalRound
        fields = ['player_one', 'player_two', 'winner', 'loser']

class SemiFinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemiFinal
        fields = ['semi_one', 'semi_two', 'semi_three', 'semi_four']

class Tournament8PSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)
    final_round = FinalRoundSerializer()
    semi_finals = SemiFinalSerializer()

    class Meta:
        model = Tournament8P
        fields = ['players', 'final_round', 'semi_finals', 'tournament_type']

    def create(self, validated_data):
        players_data = validated_data.pop('players')
        final_round_data = validated_data.pop('final_round')
        semi_finals_data = validated_data.pop('semi_finals')

        # Create Players
        players = [Player.objects.create(**player_data) for player_data in players_data]

        # Create Final Round
        final_round = FinalRound.objects.create(
            player_one=players[0],
            player_two=players[1],
            winner=players[0] if final_round_data['winner'] == players[0].name else players[1],
            loser=players[1] if final_round_data['loser'] == players[1].name else players[0],
        )

        # Create Semi Finals
        semi_finals = SemiFinal.objects.create(
            semi_one=players[2],
            semi_two=players[3],
            semi_three=players[4],
            semi_four=players[5]
        )

        # Create Tournament
        tournament = Tournament8P.objects.create(
            final_round=final_round,
            semi_finals=semi_finals,
            tournament_type=validated_data.get('tournament_type', '8P')
        )
        tournament.players.set(players)  # Assign players to the tournament

        return tournament
