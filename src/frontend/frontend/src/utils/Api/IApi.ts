export type ResponseKey = 'data' | 'status' | 'headers' | 'config' | 'request'

export interface ApiResponse<T> {
  data?: T
  status?: number
  headers?: Record<any, any>
  config?: any
  request?: any
}

export interface IApi {
  get<Tresponse>(
    url: string,
    request: ResponseKey[],
    headers?: { [key: string]: string } | Record<string, any>
  ): Promise<ApiResponse<Tresponse>>

  post<TResponse>(
    url: string,
    data: Record<string, any>,
    request: ResponseKey[],
    headers?: { [key: string]: string } | Record<string, any>
  ): Promise<ApiResponse<TResponse>>

  delete<Tresponse>(
    url: string,
    request: ResponseKey[],
    Params?: Record<string, any>
  ): Promise<ApiResponse<Tresponse>>

  setAccessToken(token: string | null): void
  removeAccessToken(): void
}
