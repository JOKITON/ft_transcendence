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

  constructor(url: string = 'ws://localhost/api/v1/livechat/ws/chat/', room: string = 'test_room') {
    this.initializeWebSocket(url, room)
  }

  private initializeWebSocket(url: string, room: string) {
    this.ws = new WebsocketBuilder(url + room)
      .withBuffer(new ArrayQueue()) // Buffer messages when disconnected
      .withBackoff(new ConstantBackoff(1000)) // Retry every 1s
      .build()
    // Event listeners
    this.ws.addEventListener(WebsocketEvent.open, this.onOpen.bind(this))
    this.ws.addEventListener(WebsocketEvent.close, this.onClose.bind(this))
    this.ws.addEventListener(WebsocketEvent.error, this.onError.bind(this))
  }

  public close(): void {
    if (this.ws) {
      this.ws.close()
    }
  }

  public send(username: string, message: string): void {
    if (this.ws) {
      this.ws.send(JSON.stringify({ username: username, message: message }))
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
    console.log('WebSocket connection error')
  }
}
