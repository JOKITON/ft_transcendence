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
    
    # Concatenar el nombre del usuario con el mensaje
    full_message = f"{username}: {message}"
    
    # Buscar el último mensaje en esa sala
    last_message = Message.objects.filter(room=room).order_by('-id').first()
    if last_message and last_message.message == full_message:
        return None
    
    # Si el mensaje es diferente, lo creas
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
