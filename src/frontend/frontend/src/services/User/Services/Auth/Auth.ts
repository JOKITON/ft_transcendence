import Api from '../../../../utils/Api/Api'
import type IAuth from '@/services/User/Services/Auth/IAuth'

export default class Auth<Trequest, Tresponse> implements IAuth<Trequest, Tresponse> {
  private api: Api<Trequest, Tresponse> = new Api()

  constructor() {}

  public async setAuthHeader<Token>(
    url: string = 'token/verify'
  ): Promise<Record<string, string> | any> {
    const accessToken = localStorage.getItem('access_token')
    if (accessToken) {
      return await this.api.get<Token>(url, { accessToken })
    }
  }

  public async checkAndRefreshToken(): Promise<boolean | any> {
    try {
      const response = await this.setAuthHeader()
      if (response) {
        console.log(response)
        return response
      }
      console.log(response)
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
