from channels.db import database_sync_to_async


@database_sync_to_async
def create_room(room):
    from .models import Room

    if Room.objects.filter(room=room).exists():
        room = Room.objects.get(room=room)
        return room
    room, _ = Room.objects.get_or_create(room=room)
    room.save()
    return room


@database_sync_to_async
def create_message(room_name, message, username, index):
    from .models import Message, Room

    room = Room.objects.get(room=room_name)
    msg = Message.objects.create(room=room, message=message, user=username, index=index)
    msg.save()
    return msg


@database_sync_to_async
def get_messages(room_name):
    from .models import Message, Room

    try:
        room = Room.objects.get(room=room_name)
        if not room:
            return []
        return list(Message.objects.filter(room=room).order_by("id"))
    except Message.DoesNotExist:
        return []
