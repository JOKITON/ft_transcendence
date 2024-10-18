import { WebsocketEvent, Websocket } from 'websocket-ts'

export default interface ISocket {
  close(): void
  send(useranem: string, message: string): void
  AddEventListener(event: WebsocketEvent, callback: () => void): void
  RemoveEventListener(event: WebsocketEvent, callback: () => void): void
}
