import type { IApi, ApiResponse, ResponseKey } from './IApi'
import type { AxiosInstance, AxiosResponse } from 'axios'
import type { AxiosError } from 'axios'
import axios from 'axios'

export default class Api implements IApi {
  private api: AxiosInstance

  constructor(
    withCredentials: boolean = false,
    url: string = 'http://localhost:3000/api/v1',
    headers: { [key: string]: string } = {
    }
  ) {
    this.api = axios.create({
      baseURL: url,
      headers: headers,
      withCredentials: withCredentials
    })
  }

  public setAccessToken(token: string | null = localStorage.getItem('access_token')): void {
    if (token) this.api.defaults.headers['Authorization'] = `Bearer ${token}`
  }

  public removeAccessToken(): void {
    delete this.api.defaults.headers.Authorization
  }

  public async get<TResponse>(
    url: string,
    request: ResponseKey[] = ['data', 'status'],
    headers?: { [key: string]: string } | Record<string, any>
  ): Promise<ApiResponse<TResponse>> {
    const accessToken = localStorage.getItem('access_token');
    this.setAccessToken(accessToken);
    return await this.api
      .get<TResponse>(url, { headers: headers })
      .then((response) => this.formatResponse(response, request))
      .catch((error) => this.handleError<TResponse>(error))
  }

  public async post<TResponse>(
    url: string,
    data?: Record<string, any>,
    request: ResponseKey[] = ['data', 'status'],
    headers?: { [key: string]: string } | Record<string, any>
  ): Promise<ApiResponse<TResponse>> {
    return await this.api
      .post<TResponse>(url, data, { headers: headers })
      .then((response) => this.formatResponse(response, request))
      .catch((error) => this.handleError<TResponse>(error))
  }

  public async delete<TResponse>(
    url: string,
    request: ResponseKey[] = ['data', 'status'],
    headers?: { [key: string]: string } | Record<string, any>
  ): Promise<ApiResponse<TResponse>> {
    return await this.api
      .delete<TResponse>(url, { headers: headers })
      .then((response) => this.formatResponse(response, request))
      .catch((error) => this.handleError<TResponse>(error))
  }

  private switchResponse<T>(response: AxiosResponse<T>, requests?: ResponseKey[]): ApiResponse<T> {
    if (!requests || !requests.length) {
      return {
        ...response.data,
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
    if (request && request?.length > 0 && response) return this.switchResponse(response, request)

    return {
      ...response.data,
      status: response.status,
      headers: response.headers,
      config: response.config,
      request: response.request
    }
  }

  private handleError<T>(error: AxiosError): ApiResponse<T> {
    const response: AxiosResponse<unknown, any> | undefined = error.response
    return {
      ...(response?.data ?? {}),
      status: response?.status ?? 500,
      headers: response?.headers ?? {},
      config: response?.config ?? {},
      request: response?.request ?? {}
    }
  }
}
