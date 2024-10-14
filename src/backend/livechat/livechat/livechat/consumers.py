from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
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

            username = text_data_json.get("username", "Anonymous")
            # Usa 'Anonymous' si no se proporciona el nombre
            message = text_data_json.get("message")

            if not message:
                await self.send(
                    text_data=json.dumps(
                        {"error": "El mensaje no puede estar vacío."})
                )
                return

            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat_message", "username": username, "message": message},
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

    async def chat_message(self, event):
        # Enviar el mensaje recibido del grupo a través del WebSocket
        await self.send(
            text_data=json.dumps(
                {"username": event["username"], "message": event["message"]}
            )
        )
