export interface token {
  token: string
  refresh: string
}

export interface tokenRequest {
  token: string
}

export interface tokenRefreshRequest {
  refresh: string
}

export interface tokenResponse {
  detail?: string
  status?: number
  token?: string
  code?: string
}
