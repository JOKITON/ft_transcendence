import hashlib


def generate_chat_id(user_id, friend_id):
    sorted_ids = sorted([str(user_id), str(friend_id)])
    concatenated_ids = f"{sorted_ids[0]}-{sorted_ids[1]}"
    chat_id = hashlib.sha1(concatenated_ids.encode()).hexdigest()[:25]
    return chat_id
