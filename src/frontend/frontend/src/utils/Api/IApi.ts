export default interface IApi {
  get<Tresponse>(url: string, Params?: Record<string, any>): Promise<Tresponse>
  post<Tresponse>(url: string, data: Record<string, any>): Promise<Tresponse>
  delete(url: string, Params?: Record<string, any>): Promise<any>
  setAccessToken(token: string | null): void
}
