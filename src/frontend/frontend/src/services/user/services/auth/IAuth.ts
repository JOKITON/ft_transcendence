export default interface IAuth {
  checkAndRefreshToken(data: Record<string, any>): Promise<boolean>
}
