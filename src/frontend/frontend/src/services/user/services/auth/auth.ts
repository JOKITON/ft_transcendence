import type IAuth from './IAuth'
import Api from '../../../../utils/Api/Api'
import type { ApiResponse } from '@/utils/Api/IApi'

export default class auth implements IAuth {
  private api: Api = new Api()

  constructor(api?: Api) {
    if (api) this.api = api
  }

  public async checkAndRefreshToken<TResponse>(): Promise<boolean> {
    try {
      const response: ApiResponse<TResponse> | ApiResponse<null> = await this.api.post<TResponse>(
        'token/verify',
        {
          token: localStorage.getItem('access') as string
        },
        ['status'],
        {
          Authorization: `Bearer ${localStorage.getItem('access') as string}`
        }
      )
      console.log('checkAndRefreshToken', response)
      if (response && response.status === 200) return true
      else {
        const refresh: ApiResponse<TResponse> | ApiResponse<null> = await this.api.post<TResponse>(
          'token/refresh',
          {
            refresh: localStorage.getItem('refresh')
          }
        )
        localStorage.setItem('access', refresh.access)
        localStorage.setItem('refresh', refresh.refresh)
        this.api.setAccessToken(refresh.access)
        if (refresh && refresh.status === 200) {
          this.checkAndRefreshToken()
        } else {
          localStorage.removeItem('access')
          localStorage.removeItem('refresh')
          console.error('Error refreshing token:', refresh)
          return false
        }
      }
      return false
    } catch (error: any) {
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      console.error('Error checking token:', error)
      return false
    }
  }
}
