export interface token {
  accessToken: string
  refreshToken: string
}

export interface tokenRequest {
  token: string
}

export interface tokenResponse {
  message?: string
  status?: number
}
