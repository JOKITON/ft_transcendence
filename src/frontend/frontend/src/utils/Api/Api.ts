import type IApi from './IApi'
import axios, { type AxiosInstance, type AxiosResponse } from 'axios'
//import Logger from '../Logger/Logger'

export default class Api<Trequest, Tresponse> implements IApi<Trequest> {
  private api: AxiosInstance
  // private logger: Logger = new Logger()

  constructor(
    url: string = 'http://localhost/api/',
    headers: { [key: string]: string } = {
      'Content-Type': 'application/json',
      Accept: 'application/json' // <- pongo ejemplo para meter mas datos al headers de la api
    },
    withCredentials: boolean = true
  ) {
    this.api = axios.create({
      baseURL: url,
      headers: headers,
      withCredentials: withCredentials
    })
  }

  public async get<Tresponse>(url: string, Params?: Record<string, any>): Promise<Tresponse> {
    try {
      console.log('url', url)
      const response: AxiosResponse<Tresponse> = await this.api.post<Tresponse>(url, { Params })
      return response.data
    } catch (e: any) {
      console.error(e)
      return <Tresponse>{}
    }
  }
  public async post<Tresponse>(url: string, data: Trequest): Promise<Tresponse> {
    try {
      const response: AxiosResponse<Tresponse> = await this.api.post<Tresponse>(url, data)
      return response.data
    } catch (e: any) {
      console.error(e)
      return <Tresponse>{}
    }
  }

  public async delete(url: string, Params?: Record<string, any>): Promise<any> {
    try {
      const response: AxiosResponse<Tresponse> = await this.api.post<Tresponse>(url, { Params })
      return response.data
    } catch (e: any) {
      console.error(e)
      return <Tresponse>{}
    }
  }
}
