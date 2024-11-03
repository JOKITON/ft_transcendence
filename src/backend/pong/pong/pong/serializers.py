from rest_framework import serializers
from django.db.models import Q
from .models import PongGame, Tournament8P
from .models import Player, FinalRound, SemiFinal, Tournament8P, Tournament4P

class PongGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PongGame
        fields = ['status', 'winner', 'player_ids', 'player_names', 'player_scores', 'player_hits', 'time_played', 'tournament_type']

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
            player.time_played += player_data['time_played']
            player.hits += player_data['player_hits']
        else:
            # For a new player, the average score is the current score
            player.scores.append(player_data['score_player'])
            player.total_score = player_data['score_player']
            player.time_played = player_data['time_played']
            player.hits = player_data['player_hits']

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
        time_played = validated_data['time_played']
        player_hits = validated_data['player_hits']
        winner = validated_data['winner']
        tournament_type = validated_data['tournament_type']
        status = validated_data['status']
        
        if status != 'C':
            raise serializers.ValidationError("Status must be 'C'")
        
        players = []

        # Iterate over the lists to create player_data dictionaries
        for i in range(len(player_ids)):
            player_data = {
                'id': player_ids[i],
                'name_player': player_names[i],
                'score_player': player_scores[i],
                'time_played': time_played,
                'player_hits': player_hits[i],
                'winner': winner
            }

            # Create or update player instances
            player = self.create_player(player_data)
            players.append(player)
        
        p1, p2 = players;
        
        # Delete any existing PongGame instances that match the given data
        to_deleted_games = PongGame.objects.filter(
            player_ids=player_ids,
            tournament_type=tournament_type,
            status='P',
        )
        deleted_game_ids = list(to_deleted_games.values_list('id', flat=True))
        to_deleted_games.delete()

        # Create the PongGame instance with the Player ForeignKey relations
        tournament = PongGame.objects.create(
            status=status,
            player1=p1,
            player2=p2,
            player_ids=player_ids,
            player_hits=player_hits,
            player_names=player_names,
            player_scores=player_scores,
            time_played=time_played,
            winner=winner,
            tournament_type=tournament_type,
        )

        return tournament
    
class PongGameStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PongGame
        fields = ['status', 'player_ids', 'player_names', 'player_scores', 'player_hits', 'time_played', 'tournament_type']

    def create_player(self, player_data):
        player, created = Player.objects.get_or_create(
            id=player_data['id'],  # Match by ID
            defaults={
                'name': player_data['name_player'],
                'total_games': 0,
                'total_score': 0,
            }
        )

        player.save()

        return player

    def create(self, validated_data):
        # Extract lists of player IDs, names, and scores
        player_ids = validated_data['player_ids']
        player_names = validated_data['player_names']
        player_scores = validated_data['player_scores']
        time_played = validated_data['time_played']
        player_hits = validated_data['player_hits']
        tournament_type = validated_data['tournament_type']
        status = validated_data['status']

        if status != 'P':
            raise serializers.ValidationError("Status must be 'P'")
        
        players = []

        # Iterate over the lists to create/update player_data dictionaries
        for i in range(len(player_ids)):
            player_data = {
                'id': player_ids[i],
                'name_player': player_names[i],
            }

            # Create or update player instances
            player = self.create_player(player_data)
            players.append(player)
        
        p1, p2 = players;

        # Create the PongGame instance with the Player ForeignKey relations
        tournament, created = PongGame.objects.get_or_create(
            player_ids=player_ids,
            tournament_type=tournament_type,
            status=status,
            defaults={
                'status': status,
                'player1': p1,
                'player2': p2,
                'player_hits': player_hits,
                'player_names': player_names,
                'player_scores': player_scores,
                'time_played': time_played,
                'tournament_type': tournament_type,
            }
        )
        
        if not created:
            tournament.player_hits = player_hits
            tournament.player_scores = player_scores
            tournament.time_played = time_played
            tournament.save()
        else:
            tournament.player_ids = player_ids
            tournament.save()
        return tournament

class PlayerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # Ensure id is included and not required
    position = serializers.IntegerField(source='last_position')  # Map 'last_position' to 'position' in the model

    class Meta:
        model = Player
        fields = ['id', 'name', 'scores', 'position', 'time_played', 'hits']

class FinalRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalRound
        fields = ['player_one', 'player_two', 'winner', 'loser']

class SemiFinalSerializer(serializers.ModelSerializer):
    class Meta: 
        model = SemiFinal
        fields = ['semi_one', 'semi_two', 'semi_three', 'semi_four']

class Tournament4PSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)
    final_round = FinalRoundSerializer()

    class Meta:
        model = Tournament4P
        fields = ['status', 'tournament_type', 'time_played' ,'players', 'final_round',  'player_ids', 'player_names', 'player_scores', 'player_hits']
        
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
            player.hits += player_data['hits']
            player.time_played += player_data['time_played']
            
            # Update the position to create the average
            player.avg_position = (player.avg_position + player_data['last_position']) / 2
        else:
            # Initialize the scores array with the current scores
            player.scores = player_data['scores']
            player.total_score = sum(player_data['scores'])
            player.total_games = len(player_data['scores'])
            player.hits = player_data['hits']
            # Create first position
            player.avg_position = player_data['last_position']
            player.time_played = player_data['time_played']

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
        status = validated_data['status']
        tournament_type = validated_data['tournament_type']
        player_ids = validated_data['player_ids']
        player_names = validated_data['player_names']
        player_scores = validated_data['player_scores']
        player_hits = validated_data['player_hits']
        time_played = validated_data['time_played']
        
        if status != 'C':
            raise serializers.ValidationError("Status must be 'C'")

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
        
        # Delete any existing Tournament4P instances that match the given data
        to_deleted_games = Tournament4P.objects.filter(
            player_ids=player_ids,
            tournament_type=tournament_type,
            status='P',
        )
        deleted_game_ids = list(to_deleted_games.values_list('id', flat=True))
        to_deleted_games.delete()

        # Create Tournament
        tournament = Tournament4P.objects.create(
            status=status,
            final_round=final_round,
            tournament_type=validated_data.get('tournament_type', '4P'),
            time_played=time_played,
            player_ids=player_ids,
            player_names=player_names,
            player_scores=player_scores,
            player_hits=player_hits,
        )
        tournament.players.set(players)  # Assign players to the tournament

        return tournament
    
class Tournament4PStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tournament4P
        fields = ['status', 'tournament_type', 'game_index', 'final_players', 'time_played', 'player_scores', 'player_ids', 'player_names', 'player_hits']
        extra_kwargs = {
            'final_players': {'required': False, 'allow_null': True}
        }
 
    def create_player(self, player_data):
        player, created = Player.objects.get_or_create(
            id=player_data['id'],  # Match by ID
            defaults={
                'name': player_data['name'],
                'total_games': 0,
                'total_score': 0,
            }
        )

        player.save()

        return player

    def create(self, validated_data):
        final_players = validated_data['final_players']
        player_ids = validated_data['player_ids']
        status = validated_data['status']
        player_names = validated_data['player_names']
        player_scores = validated_data['player_scores']
        player_hits = validated_data['player_hits']
        game_index = validated_data['game_index']
        time_played = validated_data['time_played']
        tournament_type = validated_data['tournament_type']
        
        if status != 'P':
            raise serializers.ValidationError("Status must be 'P' (Pending)")

        players = []
        for i in range(len(player_ids)):
            player_data = {
                'id': player_ids[i],
                'name': player_names[i],
            }
            player = self.create_player(player_data)
            players.append(player)
        
        # Create the PongGame instance with the Player ForeignKey relations
        tournament, created = Tournament4P.objects.get_or_create(
            player_ids=player_ids,
            tournament_type=tournament_type,
            status=status,
            defaults={
                'status': status,
                'game_index': game_index,
                'player_ids': player_ids,
                'player_names': player_names,
                'player_hits': player_hits,
                'time_played': time_played,
                'tournament_type': tournament_type,
                'final_players': final_players,
            }
        )
        
        if not created:
            tournament.player_hits = player_hits
            tournament.player_scores = player_scores
            tournament.time_played = time_played
            tournament.game_index = game_index
            tournament.final_players = final_players
        tournament.player_scores = player_scores
        tournament.players.set(players)  # Assign players to the tournament
        tournament.save()

        return tournament

class LeaderBoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ['id', 'name', 'wins']

class Tournament8PSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)
    final_round = FinalRoundSerializer()
    semi_finals = SemiFinalSerializer()

    class Meta:
        model = Tournament8P
        fields = ['status', 'players', 'final_round', 'semi_finals', 'tournament_type']

    def create(self, validated_data):
        status = validated_data['status']
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
            status=status,
            players=players,
            final_round=final_round,
            semi_finals=semi_finals,
            tournament_type=validated_data.get('tournament_type', '8P')
        )
        tournament.players.set(players)  # Assign players to the tournament

        return tournament