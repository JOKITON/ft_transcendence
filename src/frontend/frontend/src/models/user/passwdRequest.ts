export interface passwdRequest {
    currentPassword: string
    newPassword: string
    confirmPassword: string
  }

export interface passwdResponse {
  message?: string
  error?: string
} 