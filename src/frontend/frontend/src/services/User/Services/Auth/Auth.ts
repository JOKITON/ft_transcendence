import Api from '@/utils/Api/Api'
import type token from '@/Models/User/token'

export default class Auth<Trequest, token> {
  private api: Api<Trequest, token> = new Api()

  constructor() {}

  /*
  public async setAuthHeader<Token>(): Promise<token> {
    const accessToken = localStorage.getItem('access_token')
    if (accessToken) {
      return await this.api.setAuthHeader(ac
    }
  }

  public async refreshAuthToken<Token>(): Promise<boolean> {
    try {
      const response = await this.api.post<Token>('user/token/refresh/', {
        withCredentials: true
      })

      const newAccessToken = response.data.access
      if (newAccessToken) {
        localStorage.setItem('access_token', newAccessToken)
      }

      return true
    } catch (error) {
      console.error('Refresh token error:', error.response ? error.response.data : error.message)
      alert('Session expired. Please log in again.')
      return false
    }
  }*/
}
