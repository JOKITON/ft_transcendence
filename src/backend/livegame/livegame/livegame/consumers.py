from channels.generic.websocket import AsyncWebsocketConsumer
import json


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            player_1 = text_data_json.get("player_1")
            player_2 = text_data_json.get("player_1")
            game = text_data_json.get("game")

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "game",
                    "player_1": {
                        "y": player_1["y"],
                        "x": player_1["x"],
                    },
                    "player_2": {
                        "y": player_2["y"],
                        "x": player_2["x"],
                    },
                    "game": {
                        "y": game["y"],
                        "x": game["x"],
                        "z": game["z"],
                    },
                },
            )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON format"}))

    async def game(self, event):
        text_data = json.dumps(
            {
                "event": "message",
                "player_1": event["player_1"],
                "player_2": event["player_2"],
                "game": event["game"],
            }
        )
        await self.send(text_data=text_data)
