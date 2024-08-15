import type { token } from './token'

export interface UserResponse {
  message: string
  status: number
  token?: token
}
