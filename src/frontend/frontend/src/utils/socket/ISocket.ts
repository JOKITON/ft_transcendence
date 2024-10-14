import { WebsocketEvent, Websocket } from 'websocket-ts'

export default interface ISocket {
  close(): void
  send(message: Record<string, unknown>): void
  AddEventListener(event: WebsocketEvent, callback: () => void): void
  RemoveEventListener(event: WebsocketEvent, callback: () => void): void
}
