export interface userDataRequest {
  newUsername: string
  newNickname: string
  newEmail: string
}

export interface userDataResponse {
  message?: string
  error?: string
}
