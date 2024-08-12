export default interface IAuth<Trequest, Tresponse> {
  setToken(token: string): void
  refreshAuthToken(): Promise<boolean>
  checkAndRefreshToken(): Promise<boolean>
}
