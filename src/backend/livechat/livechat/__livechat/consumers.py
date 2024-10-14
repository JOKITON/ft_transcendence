from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import sync_to_async
import json
# from jwt_auth.authentication import JWTAuthentication
# from rest_framework.permissions import IsAuthenticated


class ConsumerLiveChat(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.user_inbox = None

    """ hay que verificar el token del usuario para que pueda conectarse a la sala"""

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = self.room_name
        try:
            from .models import Room

            room = sync_to_async(Room.objects.get(name=self.room_name))
            # el usuario  tiene que estar en la sala
            self.room = room
            print("connected")
            self.accept()
        except Exception as e:
            self.close()
            raise Exception(f"Room not exists {e}")

    def disconnect(self, close_code):
        print(f"disconnected {close_code}")

    def receive(self, text_data):
        if not text_data:
            print("No data")
            return  # Maneja el caso de mensaje vacío

        print(f"received {text_data}")
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))


"""
class ConsumerLiveChat(AsyncWebsocketConsumer):
    seteo la variable room_name, room_group_name, room, user, user_inbox a None

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.user_inbox = None

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        try:
            room = Room.objects.get(name=self.room_name)
            # el usuario  tiene que estar en la sala
            room.filter(online=self.scope["user"])
            self.room = room
        except Exception as e:
            await self.close()
            raise Exception(f"Room not exists {e}")

        if self.scope["user"].is_authenticated:
            self.user = self.scope["user"]
            self.user_inbox = f"inbox_{self.user.username}"
            await self.channel_layer.group_add(self.user_inbox, self.channel_name)

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        print("Received", text_data, bytes_data)
        msg = Message.objects.create(
            user=self.user, room=self.room, message=text_data)
        msg.save()
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": msg}
        )

        await self.send(text_data=json.dumps({"message": message}))

    async def disconnect(self, close_code):
        if self.user is not None:
            await self.channel_layer.group_discard(self.user_inbox, self.channel_name)
        await self.close()
"""
