from rest_framework import serializers
from .models import PongGame, Tournament8P
from .models import Player, FinalRound, SemiFinal, Tournament8P

"""     def to_internal_value(self, data):
        # Convert player1, player2, and winner nicknames to Player instances
        data = data.copy()  # Make a mutable copy of the data

        data['player1'] = self.get_player_by_name(data.get('player1'))
        data['player2'] = self.get_player_by_name(data.get('player2'))
        data['winner'] = self.get_player_by_name(data.get('winner'))

        return super().to_internal_value(data) """

class PongGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PongGame
        fields = ['winner', 'name_player1', 'name_player2', 'id_player1', 'id_player2', 'score_player1', 'score_player2', 'tournament_type']

    def get_player_by_id(self, player_id):
        try:
            # Fetch the Player instance by its ID
            return Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            raise serializers.ValidationError(f"Player with ID '{player_id}' does not exist.")
    
    def create_players(self, player_data):
        player1 = self.get_player_by_id(player_data['id_player1'])
        player2 = self.get_player_by_id(player_data['id_player2'])

        # Update scores and stats
        player1.score += player_data['score_player1']
        player2.score += player_data['score_player2']

        if player_data['winner'] == player_data['name_player1']:
            player1.wins += 1
            player2.losses += 1
        else:
            player2.wins += 1
            player1.losses += 1

        player1.total_games += 1
        player2.total_games += 1

        player1.save()
        player2.save()

        return player1, player2

    def create(self, validated_data):
        # Extract and remove player info from validated_data
        player_data = {
            'id_player1': validated_data.pop('id_player1'),
            'id_player2': validated_data.pop('id_player2'),
            'name_player1': validated_data['name_player1'],
            'name_player2': validated_data['name_player2'],
            'score_player1': validated_data['score_player1'],
            'score_player2': validated_data['score_player2'],
            'winner': validated_data['winner']
        }
        
        # Create or update players
        p1, p2 = self.create_players(player_data)
        
        # Create the PongGame instance with proper Player foreign keys
        tournament = PongGame.objects.create(
            id_player1=p1, id_player2=p2, **validated_data
        )
        return tournament

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
