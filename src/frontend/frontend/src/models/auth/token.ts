export interface token {
  access: string
  refresh: string
  status?: number
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
  token?: token
  code?: string
}
