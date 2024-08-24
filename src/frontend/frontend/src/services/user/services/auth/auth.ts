import type { token, tokenRequest } from '@/models/auth/token'
import type { userResponse } from '@/models/user/userResponse'
import type { ApiResponse } from '@/utils/Api/IApi'
import Api from '../../../../utils/Api/Api'
import type IAuth from './IAuth'
import axios from 'axios'

export default class auth implements IAuth {
  private api: Api = new Api()

  constructor(api?: Api) {
    if (api) this.api = api
  }

  public async login(data: Record<string, any>): Promise<boolean> {
    try {
      const response: ApiResponse<userResponse> = await this.api.post<userResponse>('login', data)
      if (response && response?.status === 200) {
        this.setToken(response?.token as token)
        this.api.setAccessToken(response.token?.access)
        return true
      }
      return false
    } catch (error: any) {
      console.error('Error logging in:', error)
      return false
    }
  }

  public async checkAndRefreshToken(): Promise<boolean> {
    try {
      const response: boolean = await this.verifyToken()
      if (response === true) return true
      else {
        const refresh: ApiResponse<token> = await this.api.post<token>('token/refresh', {
          refresh: localStorage.getItem('refresh')
        })

        this.setToken(refresh as token)
        this.api.setAccessToken(refresh?.refresh)
        if (refresh && refresh.status === 200) {
          if (true === (await this.verifyToken())) return true
        } else {
          this.removeToken()
          console.error('Error refreshing token:', refresh)
          return false
        }
      }
      return false
    } catch (error: any) {
      this.removeToken()
      console.error('Error checking token:', error)
      return false
    }
  }

  private async verifyToken(): Promise<boolean> {
    try {
      const response: ApiResponse<tokenRequest> = await this.api.post<tokenRequest>(
        'token/verify',
        {
          token: localStorage.getItem('access') as string
        },
        ['status'],
        {
          Authorization: `Bearer ${localStorage.getItem('access') as string}`
        }
      )

      if (response && response?.status === 200) return true
      else return false
    } catch (error: any) {
      this.removeToken()
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 401) {
          console.error('Token expired:', error)
          return false
        }
      }
      console.error('Error checking token:', error)
      return false
    }
  }

  private setToken(token: token): void {
    localStorage.setItem('access', token?.access)
    localStorage.setItem('refresh', token?.refresh)
  }

  private removeToken(): void {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
  }
}
