from django.test import TestCase
from pong.models import Round
from pong.serializers import RoundSerializer


class RoundTestCase(TestCase):
    def setUp(self):
        Round.objects.create(
            player1="player1", player2="player2", score1=21, score2=19, win=True
        )
        Round.objects.create(
            player1="player1", player2="player2", score1=21, score2=19, win=True
        )

    def test_rounds(self):
        round1 = Round.objects.get(player1="player1")
        round2 = Round.objects.get(player2="player2")
        self.assertEqual(round1.player1, "player1")
        self.assertEqual(round2.player2, "player2")
        self.assertEqual(round1.score1, 21)
        self.assertEqual(round2.score2, 19)
        self.assertEqual(round1.win, True)
        self.assertEqual(round2.win, True)

        # llamada a la api para obtener los RoundSerializer con datos aleatorios

    class RoundSerializerTestCase(TestCase):
        def setUp(self):
            self.round = Round.objects.create(
                player1="player1", player2="player2", score1=21, score2=19, win=True
            )

        def test_round_serializer(self):
            serializer = RoundSerializer(self.round)
            self.assertEqual(
                serializer.data,
                {
                    "id": self.round.id,
                    "player1": "player1",
                    "player2": "player2",
                    "score1": 21,
                    "score2": 19,
                },
            )

        def test_round_serializer_empty(self):
            serializer = RoundSerializer()
            self.assertEqual(serializer.data, {})
