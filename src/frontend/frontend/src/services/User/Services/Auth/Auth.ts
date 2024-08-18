import type IAuth from '@/services/User/Services/Auth/IAuth'
import Api from '../../../../utils/Api/Api'

export default class Auth implements IAuth {
  private api: Api = new Api()

  constructor(api?: Api) {
    if (api) this.api = api
  }

  public async checkAndRefreshToken<Tresponse>(data: Record<string, any>): Promise<Tresponse> {
    try {
      const response: Tresponse = await this.api.post<Tresponse>('token/verify', data)
      console.log('Token response:', response)
      return response
    } catch (error: any) {
      console.error('Error checking token:', error)
      return error
    }
  }
}
