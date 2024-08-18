import type { AxiosError } from 'node_modules/axios/index.cjs'
import axios, { type AxiosInstance, type AxiosResponse } from 'axios'
import type IApi from './IApi'

export default class Api implements IApi {
  private api: AxiosInstance

  constructor(
    url: string = 'http://localhost/api/',
    headers: { [key: string]: string } = {
      'Content-Type': 'application/json',
      Accept: 'application/json' // <- pongo ejemplo para meter mas datos al headers de la api
    },
    withCredentials: boolean = false
  ) {
    this.api = axios.create({
      baseURL: url,
      headers: headers,
      withCredentials: withCredentials
    })
  }

  public setAccessToken(token: string | null = localStorage.getItem('accessToken')): void {
    if (token) this.api.defaults.headers.Authorization = `Bearer ${token}`
  }

  public async get<Tresponse>(url: string, data: Record<string, any>): Promise<Tresponse> {
    try {
      const response: AxiosResponse<Tresponse> = await this.api.get<Tresponse>(url, data)
      return response.data
    } catch (error: any) {
      if (axios.isAxiosError(error)) {
        console.error('Axios error: ', error)
      } else {
        console.error('Unexpected error: ', error)
      }
      throw error
    }
  }

  public async post<Tresponse>(url: string, data: Record<string, any>): Promise<Tresponse> {
    try {
      const response: AxiosResponse<Tresponse> = await this.api.post<Tresponse>(url, data)
      console.log('response: ', response)
      return response.data
    } catch (error: any | AxiosError) {
      if (axios.isAxiosError(error)) {
        console.error('Axios error: ', error)
      } else {
        console.error('Unexpected error: ', error)
      }
      throw error.response.data
    }
  }

  public async delete<Tresponse>(url: string, data: Record<string, any>): Promise<Tresponse> {
    try {
      const response: AxiosResponse<Tresponse> = await this.api.delete<Tresponse>(url, data)
      return response.data
    } catch (error: any) {
      if (axios.isAxiosError(error)) {
        console.error('Axios error: ', error)
      } else {
        console.error('Unexpected error: ', error)
      }
      throw error
    }
  }
}
