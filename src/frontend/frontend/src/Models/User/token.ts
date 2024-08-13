export interface token {
  accessToken: string
  refreshToken: string
}

export interface tokenVerify {
  token: string
  withCredentials: boolean
}
