import type { AxiosError } from 'axios'
import type { IApi, ApiResponse, ResponseKey } from './IApi'
import type { AxiosInstance, AxiosResponse } from 'axios'
import axios from 'axios'

export default class Api implements IApi {
  private api: AxiosInstance

  constructor(
    withCredentials: boolean = false,
    url: string = 'http://localhost/api/v1',
    headers: { [key: string]: string } = {
      'Content-Type': 'application/json',
      Accept: 'application/json'
    }
  ) {
    this.api = axios.create({
      baseURL: url,
      headers: headers,
      withCredentials: withCredentials
    })
  }

  public setAccessToken(token: string | null = localStorage.getItem('accessToken')): void {
    if (token) {
      this.api.defaults.headers.Authorization = `Bearer ${token}`
    }
  }

  public removeAccessToken(): void {
    delete this.api.defaults.headers.Authorization
  }

  public async get<TResponse>(
    url: string,
    request?: ResponseKey[],
    headers?: { [key: string]: string } | Record<string, any>
  ): Promise<ApiResponse<TResponse> | ApiResponse<null>> {
    return await this.api
      .get<TResponse>(url, { headers: headers })
      .then((response) => this.formatResponse(response, request))
      .catch((error) => this.handleError(error))
  }

  public async post<TResponse>(
    url: string,
    data?: Record<string, any>,
    request?: ResponseKey[],
    headers?: { [key: string]: string } | Record<string, any>
  ): Promise<ApiResponse<TResponse> | ApiResponse<null>> {
    return await this.api
      .post<TResponse>(url, data, { headers: headers })
      .then((response) => this.formatResponse(response, request))
      .catch((error) => this.handleError(error))
  }

  public async delete<TResponse>(
    url: string,
    request?: ResponseKey[],
    headers?: { [key: string]: string } | Record<string, any>
  ): Promise<ApiResponse<TResponse> | ApiResponse<null>> {
    return await this.api
      .delete<TResponse>(url, { headers: headers })
      .then((response) => this.formatResponse(response, request))
      .catch((error) => this.handleError(error))
  }

  private switchResponse<T>(
    response: AxiosResponse<T>,
    requests: ResponseKey[] = []
  ): ApiResponse<T> {
    if (!requests || requests.length === 0) {
      return {
        data: response.data,
        status: response.status,
        headers: response.headers,
        config: response.config,
        request: response.request
      }
    }

    const result: ApiResponse<T> = {} as ApiResponse<T>
    requests.forEach((request) => {
      switch (request) {
        case 'data':
          //meto los objetos directamente en vez de data: {Object [...] <- concateno}
          Object.assign(result, { ...response.data })
          break
        case 'status':
          result.status = response.status
          break
        case 'headers':
          result.headers = response.headers
          break
        case 'config':
          result.config = response.config
          break
        case 'request':
          result.request = response.request
          break
        default:
          console.warn(`Unknown request key: ${request}`)
          break
      }
    })
    return result as ApiResponse<T>
  }

  private formatResponse<T>(response: AxiosResponse<T>, request?: ResponseKey[]): ApiResponse<T> {
    if (request && request?.length > 0 && response) {
      return this.switchResponse(response, request)
    }
    return {
      data: response.data,
      status: response.status,
      headers: response.headers,
      config: response.config,
      request: response.request
    }
  }

  private handleError(error: AxiosError): ApiResponse<null> {
    const response: AxiosResponse<unknown, any> | undefined = error.response
    return {
      data: null,
      status: response?.status ?? 500,
      headers: response?.headers ?? {},
      config: response?.config ?? {},
      request: response?.request ?? {}
    }
  }
}
