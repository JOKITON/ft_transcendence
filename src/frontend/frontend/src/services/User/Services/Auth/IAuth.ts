export default interface IAuth {
  checkAndRefreshToken<Tresponse>(data: Record<string, any>): Promise<Tresponse>
}
