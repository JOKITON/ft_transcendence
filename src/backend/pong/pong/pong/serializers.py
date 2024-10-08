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
        fields = ['winner', 'player_ids', 'player_names', 'player_scores', 'tournament_type']

    def create_player(self, player_data):
        player, created = Player.objects.get_or_create(
            id=player_data['id'],  # Match by ID
            name=player_data['name_player'],  # Match by name, or you can use another unique field
            defaults={'avg_score': player_data['score_player']}
        )

        if not created:
            # Calculate the new average score considering the new game's score
            total_games = player.total_games + 1
            player.avg_score = float(float(player.avg_score * player.total_games) + player_data['score_player']) / total_games
        else:
            # For a new player, the average score is the current score
            player.avg_score = player_data['score_player']

        # Update wins, losses, and total games
        if player_data['winner'] == player_data['name_player']:
            player.wins += 1
        else:
            player.losses += 1

        player.total_games += 1
        player.save()

        return player

    def create(self, validated_data):
        # Extract lists of player IDs, names, and scores
        player_ids = validated_data['player_ids']
        player_names = validated_data['player_names']
        player_scores = validated_data['player_scores']
        winner = validated_data['winner']
        
        players = []

        # Iterate over the lists to create player_data dictionaries
        for i in range(len(player_ids)):
            player_data = {
                'id': player_ids[i],
                'name_player': player_names[i],
                'score_player': player_scores[i],
                'winner': winner
            }
            print(player_data)  # Example operation

            # Create or update player instances
            player = self.create_player(player_data)
            players.append(player)
        
        p1, p2 = players;

        # Create the PongGame instance with the Player ForeignKey relations
        tournament = PongGame.objects.create(
            player1=p1,
            player2=p2,
            player_names=player_names,
            player_scores=player_scores,
            winner=winner,
        )

        return tournament

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['name', 'avg_score', 'position']

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
