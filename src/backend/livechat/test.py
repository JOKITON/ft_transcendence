import websocket
import json
import time


def on_message(ws, message):
    print("Received message:", message)


def on_error(ws, error):
    print("Error:", error)


def on_close(ws, status_code, reason):
    print("Connection closed:", status_code, reason)


def on_open(ws):
    print("Connection opened")
    # Puedes enviar un mensaje si lo deseas
    for i in range(3):
        print("Sending message")
        ws.send(json.dumps({"message": "Hola, servidor!"}))
        time.sleep(2)


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "ws://localhost/api/v1/livechat/ws/chat/room/",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()
