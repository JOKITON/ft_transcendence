import type { token } from '../auth/token'

export interface userResponse {
  message: string
  status: number
  token?: token
}
