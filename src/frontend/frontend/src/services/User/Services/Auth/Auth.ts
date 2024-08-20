import type IAuth from '@/services/User/Services/Auth/IAuth'
import Api from '../../../../utils/Api/Api'
import type { tokenResponse, token } from '@/Models/User/token'

export default class Auth implements IAuth {
  private api: Api = new Api()

  constructor(api?: Api) {
    if (api) this.api = api
  }

  public async checkAndRefreshToken<tokenResponse>(data: Record<string, any>): Promise<boolean> {
    try {
      /*if (response.code != 200) {
        return false
      } else if ((response.detail = 'Token not valid')) {
        const r: token = await this.api.post<token>('token/refresh', data)
        console.log('Refresh response:', response)
        localStorage.setItem('token', r.token)
        localStorage.setItem('refresh', r.refresh)
        return this.checkAndRefreshToken(data) // Recursive call to check the new token
      }*/
      return false
    } catch (error: any) {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      console.error('Error checking token:', error)
      return false
    }
  }
}
