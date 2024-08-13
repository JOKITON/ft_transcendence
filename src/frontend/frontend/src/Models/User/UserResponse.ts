import type { token } from './token'

export default interface UserResponse {
  message: string
  status: number
  token: token
}
