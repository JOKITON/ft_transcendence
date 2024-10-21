from channels.generic.websocket import AsyncWebsocketConsumer
from .db import create_room, create_message, get_messages
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await create_room(self.room_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send_historical_messages()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            username = text_data_json.get("username", "Anonymous")
            message = text_data_json.get("message")
            index = text_data_json.get("index")
            if not message:
                await self.send(
                    text_data=json.dumps({"error": "El mensaje no puede estar vacío."})
                )
                return

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "username": username,
                    "message": message,
                    "index": index,
                },
            )

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Formato JSON inválido."}))
        except Exception as e:
            await self.send(
                text_data=json.dumps(
                    {
                        "error": str(e)  # Manejo genérico de excepciones
                    }
                )
            )

    async def send_historical_messages(self):
        messages = await get_messages(self.room_name)
        for message in messages:
            print(message)
            text_data = json.dumps(
                {
                    "event": "message",
                    "username": message.user,
                    "message": message.message,
                    "index": message.index,
                }
            )
            await self.send(text_data=text_data)

    async def chat_message(self, event):
        await create_message(
            self.room_name, event["message"], event["username"], event["index"]
        )
        text_data = json.dumps(
            {
                "event": "message",
                "username": event["username"],
                "message": event["message"],
                "index": event["index"],
            }
        )
        await self.send(text_data=text_data)
