export default interface IAuth {
  checkAndRefreshToken(): Promise<boolean>
  login(data: Record<string, any>): Promise<boolean>
  register(data: Record<string, any>): Promise<boolean>
}
