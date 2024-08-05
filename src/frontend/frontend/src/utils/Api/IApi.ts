export default interface IApi<Trequest> {
  get<Tresponse>(url: string, Params?: Record<string, any>): Promise<Tresponse>
  post<Tresponse>(url: string, data: Trequest): Promise<Tresponse>
  delete(url: string, Params?: Record<string, any>): Promise<void>
}
