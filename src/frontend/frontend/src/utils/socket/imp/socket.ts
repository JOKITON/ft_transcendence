import {
  ArrayQueue,
  ConstantBackoff,
  Websocket,
  WebsocketBuilder,
  WebsocketEvent
} from 'websocket-ts'

import type ISocket from '../ISocket'

export default class Socket implements ISocket {
  private ws: Websocket | null = null
  private url: string
  private room: string

  constructor(
    url: string = 'wss://localhost:7102/api/v1/livechat/ws/chat/',
    room: string = 'test_room'
  ) {
    this.url = url
    this.room = room
  }

  public open(room?: string): void {
    if (this.room === 'test_room') {
      this.room = room || this.room
    }
    this.ws = new WebsocketBuilder(this.url + this.room)
      .withBuffer(new ArrayQueue()) // Buffer messages when disconnected
      .withBackoff(new ConstantBackoff(3)) // Retry every 1s
      .build()
    this.ws.addEventListener(WebsocketEvent.open, this.onOpen.bind(this))
    this.ws.addEventListener(WebsocketEvent.close, this.onClose.bind(this))
    this.ws.addEventListener(WebsocketEvent.error, this.onError.bind(this))
  }

  public close(): void {
    if (this.ws) {
      this.ws.close()
    }
  }

  public send(username: string, message: string, index: string): void {
    if (this.ws) {
      const response = JSON.stringify({ username: username, message: message, index: index })
      this.ws.send(response)
    } else {
      console.error('WebSocket is not open. Cannot send message.')
    }
  }

  public reconnect(): boolean | undefined {
    if (this.ws) {
      return this.ws.instantReconnect
    }
  }

  public AddEventListener(event: WebsocketEvent, callback: (event: Event) => void): void {
    if (this.ws) {
      this.ws.addEventListener(event, callback)
    }
  }

  public RemoveEventListener(event: WebsocketEvent, callback: (event: Event) => void): void {
    if (this.ws) {
      this.ws.removeEventListener(event, callback)
    }
  }

  private onOpen(): void {
    console.log('WebSocket connection opened')
  }

  private onClose(): void {
    console.log('WebSocket connection closed')
  }

  private onError(): void {
    this.ws?.close()
    console.log('WebSocket connection error')
  }
}
