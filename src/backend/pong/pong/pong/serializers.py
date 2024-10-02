from rest_framework import serializers
from .models import Tournament, Tournament8P
from .models import Player, FinalRound, SemiFinal, Tournament8P
from .models import PlayerStats

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['winner', 'player1', 'player2', 'score_player1', 'score_player2', 'tournament_type']
    
"""     def to_internal_value(self, data):
        # Convert player1, player2, and winner nicknames to Player instances
        data = data.copy()  # Make a mutable copy of the data

        data['player1'] = self.get_player_by_name(data.get('player1'))
        data['player2'] = self.get_player_by_name(data.get('player2'))
        data['winner'] = self.get_player_by_name(data.get('winner'))

        return super().to_internal_value(data) """

    def get_player_by_name(self, player_name):
        try:
            # Fetch the Player instance by nickname
            return Player.objects.get(name=player_name).pk
        except Player.DoesNotExist:
            raise serializers.ValidationError(f"Player with nickname '{player_name}' does not exist.")
    
    def create(self, validated_data):
        # Create and save the tournament instance
        tournament = Tournament.objects.create(**validated_data)
        # self.update_player_stats(tournament)
        return tournament

    def update_player_stats(self, tournament):
        # Get or create player stats for player1 and player2
        player1_stats, created = PlayerStats.objects.get_or_create(player=tournament.player1)
        player2_stats, created = PlayerStats.objects.get_or_create(player=tournament.player2)

        # Update total games for both players
        player1_stats.total_games += 1
        player2_stats.total_games += 1

        # Update wins and losses based on the winner
        if tournament.winner == tournament.player1:
            player1_stats.wins += 1
            player2_stats.losses += 1
        else:
            player1_stats.losses += 1
            player2_stats.wins += 1

        # Save the updated stats
        player1_stats.save()
        player2_stats.save()

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
            player_one=final_round_data['player_one'],
            player_two=final_round_data['player_two'],
            winner=final_round_data['winner'],
            loser=final_round_data['loser'],
        )

        # Create Semi Finals
        semi_finals = SemiFinal.objects.create(
            semi_one=semi_finals_data['semi_one'],
            semi_two=semi_finals_data['semi_two'],
            semi_three=semi_finals_data['semi_three'],
            semi_four=semi_finals_data['semi_four'],
        )

        # Create Tournament
        tournament = Tournament8P.objects.create(
            final_round=final_round,
            semi_finals=semi_finals,
            tournament_type=validated_data.get('tournament_type', '8P')
        )
        tournament.players.set(players)  # Assign players to the tournament

        return tournament
