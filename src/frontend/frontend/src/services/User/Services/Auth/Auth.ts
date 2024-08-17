import type IAuth from '@/services/User/Services/Auth/IAuth'
import Api from '../../../../utils/Api/Api'

export default class Auth<Trequest, Tresponse> implements IAuth<Trequest, Tresponse> {
  private api: Api<Trequest, Tresponse> = new Api<Trequest, Tresponse>()

  constructor(api?: Api<Trequest, Tresponse>) {
    if (api) this.api = api
  }

  public async checkAndRefreshToken(data: Trequest): Promise<Tresponse> {
    try {
      const response: Tresponse = await this.api.post<Tresponse>('token/verify', data)
      return response
    } catch (error: any) {
      console.error('Error checking token:', error)
      return error
    }
  }
}
