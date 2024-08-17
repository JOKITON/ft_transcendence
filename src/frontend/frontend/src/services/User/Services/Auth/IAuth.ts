export default interface IAuth<Trequest, Tresponse> {
  checkAndRefreshToken(data: Trequest): Promise<Tresponse>
}
