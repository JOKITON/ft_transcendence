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
  private room: string
  private messages: Array<Record<string, unknown>> = [] // Almacena los mensajes recibidos

  constructor(url: string = 'ws://localhost/api/v1/livechat/ws/chat/', room: string = 'test_room') {
    this.room = room
    this.ws = new WebsocketBuilder(url + this.room)
      .withBuffer(new ArrayQueue()) // buffer messages when disconnected
      .withBackoff(new ConstantBackoff(1000)) // retry every 1s
      .build()
    this.initializeWebSocket(url)
  }

  private initializeWebSocket(url: string) {
    this.ws = new WebsocketBuilder(url + this.room)
      .withBuffer(new ArrayQueue()) // Buffer messages when disconnected
      .withBackoff(new ConstantBackoff(1000)) // Retry every 1s
      .build()

    // Event listeners
    this.ws.addEventListener('open', this.onOpen.bind(this))
    this.ws.addEventListener('close', this.onClose.bind(this))
    this.ws.addEventListener('error', this.onError.bind(this))
    this.ws.addEventListener('message', this.onMessage.bind(this))
  }
  set Websocket(ws: Websocket) {
    this.ws = ws
  }

  get Websocket(): Websocket | null {
    return this.ws
  }

  public close(): void {
    if (this.ws) {
      this.ws.close()
    }
  }

  public send(message: Record<string, unknown>): void {
    if (this.ws && this.ws.readyState === Websocket.OPEN) {
      console.log('Sending message:', message)
      this.ws.send(JSON.stringify(message))
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

  private onMessage(event: MessageEvent): void {
    try {
      const data = JSON.parse(event.data)
      console.log('Received message:', data)
      this.messages.push(data) // Almacena el mensaje recibido
      this.handleNewMessage(data) // Llama a un callback o maneja el nuevo mensaje
    } catch (error) {
      console.error('Error parsing message:', error)
    }
  }

  private handleNewMessage(data: Record<string, unknown>): void {
    console.log('New message received:', data)
  }

  public getMessages(): Array<Record<string, unknown>> {
    return this.messages // Devuelve todos los mensajes recibidos
  }

  public getLastMessage(): Record<string, unknown> | null {
    return this.messages.length > 0 ? this.messages[this.messages.length - 1] : null // Devuelve el último mensaje o null si no hay mensajes
  }

  private onOpen(): void {
    console.log('WebSocket connection opened')
  }

  private onClose(): void {
    console.log('WebSocket connection closed')
  }

  private onError(event: Event): void {
    console.error('WebSocket error:', event)
  }
}
