import Api from '../../../../utils/Api/Api'
import type IAuth from '@/services/User/Services/Auth/IAuth'
import type { tokenVerify } from '../../../../Models/User/token'

export default class Auth<Trequest, Tresponse> implements IAuth<Trequest, Tresponse> {
  private api: Api<Trequest, Tresponse> = new Api()

  constructor() {}

  public async setAuthHeader(url: string = 'token/verify'): Promise<any> {
    const accessToken: String | null = localStorage.getItem('access_token')
    console.log('jwt twt   ', accessToken)
    if (accessToken) {
      const send = { token: accessToken, withCredentials: true }
      return await this.api.get<tokenVerify>(url, send)
    }
    return false
  }

  public async checkAndRefreshToken(): Promise<boolean | any> {
    try {
      const response = await this.setAuthHeader()
      if (response) {
        console.log('jwt twt   ', response)
        return response
      }
    } catch (error: any) {
      console.error('Refresh token error:', error.response ? error.response.data : error.message)
      alert('Session expired. Please log in again.')
    }
    return true
  }

  /*public async checkAndRefreshToken() {
    try {
      const accessToken = localStorage.getItem('access_token')
      if (accessToken) {
        this.setAuthHeader()
       const response = await this.api.post('token/verify/', {
        token: accessToken,
        withCredentials: true, // Ensure cookies are sent with the request
    }
    } catch (error: any) {
          console.error('Refresh token error:', error.response ? error.response.data : error.message)
          alert('Session expired. Please log in again.')
          return false
        }
        if (response.status === 200) {
          return true // Token is still valid
        }
      } else console.log('No token found. Redirecting to login.')
      return false
    } catch (error) {
      const response = error.response
    switch (response.data.code) {
      case 'expired':
        console.log('Token expired. Attempting to refresh.')
        const refreshed = await refreshAuthToken()
        return refreshed

      case 'token_not_valid':
        console.log('Token invalid. Redirecting to login.')
        removeAccessToken()
        return false

      case 'missing':
        console.log('Token missing. Redirecting to login.')
        removeAccessToken()
        return false

      default:
        console.error('Unexpected token status:', response.data.status)
        removeAccessToken()
        return false
    */
}
