import type { token } from '@/models/auth/token'

export default interface IAuth {
  checkAndRefreshToken(): Promise<boolean>
  login(data: Record<string, any>): Promise<boolean>
  logout(): Promise<boolean>
  register(data: Record<string, any>): Promise<boolean>
  setToken(token: token): void
  removeToken(): void
}
