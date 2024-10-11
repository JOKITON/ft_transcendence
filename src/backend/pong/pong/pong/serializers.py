from rest_framework import serializers
from .models import PongGame, Tournament8P
from .models import Player, FinalRound, SemiFinal, Tournament8P, Tournament4P

class PongGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PongGame
        fields = ['winner', 'player_ids', 'player_names', 'player_scores', 'tournament_type']

    def create_player(self, player_data):
        player, created = Player.objects.get_or_create(
            id=player_data['id'],  # Match by ID
            defaults={
                'name': player_data['name_player'],
                'total_games': 0,
                'total_score': 0,
            }
        )

        if not created:
            # Calculate the new average score considering the new game's score
            player.scores.append(player_data['score_player'])
            player.total_score += player_data['score_player']
        else:
            # For a new player, the average score is the current score
            player.scores.append(player_data['score_player'])
            player.total_score = player_data['score_player']

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
        tournament_type = validated_data['tournament_type']
        
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
            tournament_type=tournament_type,
        )

        return tournament

class PlayerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # Ensure id is included and not required
    position = serializers.IntegerField(source='last_position')  # Map 'last_position' to 'position' in the model

    class Meta:
        model = Player
        fields = ['id', 'name', 'scores', 'position']

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
            players=players,
            final_round=final_round,
            semi_finals=semi_finals,
            tournament_type=validated_data.get('tournament_type', '8P')
        )
        tournament.players.set(players)  # Assign players to the tournament

        return tournament

class Tournament4PSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)
    final_round = FinalRoundSerializer()

    class Meta:
        model = Tournament4P
        fields = ['players', 'final_round', 'tournament_type']
        
    def create_player(self, player_data):
        player, created = Player.objects.get_or_create(
            id=player_data['id'],
            defaults={
                'name': player_data['name'],
                'total_games': 0,
                'total_score': 0,
            }
        )

        if not created:
            # Append the new scores to the existing scores array
            player.scores = player.scores + player_data['scores']
            player.total_score += sum(player_data['scores'])
            player.total_games += len(player_data['scores'])
            
            # Update the position to create the average
            player.avg_position = (player.avg_position + player_data['last_position']) / 2
        else:
            # Initialize the scores array with the current scores
            player.scores = player_data['scores']
            player.total_score = sum(player_data['scores'])
            player.total_games = len(player_data['scores'])
            # Create first position
            player.avg_position = player_data['last_position']

        player.last_position=player_data['last_position']
        # Update wins &  losses
        if player_data['last_position'] == 1:
            player.wins += 2
        if player_data['last_position'] == 2:
            player.wins += 1
            player.losses += 1
        if player_data['last_position'] > 2:
            player.losses += 1

        player.save()
        return player

    def create(self, validated_data):
        players_data = validated_data.pop('players')
        final_round_data = validated_data.pop('final_round')

        # Create Players
        players = []
        for player_data in players_data:
            player = self.create_player(player_data)
            players.append(player)

        # Create Final Round
        final_round = FinalRound.objects.create(
            player_one=final_round_data['player_one'],
            player_two=final_round_data['player_two'],
            winner=final_round_data['winner'],
            loser=final_round_data['loser'],
        )

        # Create Tournament
        tournament = Tournament4P.objects.create(
            final_round=final_round,
            tournament_type=validated_data.get('tournament_type', '4P')
        )
        tournament.players.set(players)  # Assign players to the tournament

        return tournament
