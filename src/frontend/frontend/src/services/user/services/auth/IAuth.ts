export default interface IAuth {
  checkAndRefreshToken(): Promise<boolean>
}
