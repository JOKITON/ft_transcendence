from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import json


class LiveChat(AsyncWebsocketConsumer):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    async def send_message(self, event):
        # uso de json.dumps para convertir el mensaje a un string
        message = json.dumps(event["message"])
        await self.send(text_data=message)
