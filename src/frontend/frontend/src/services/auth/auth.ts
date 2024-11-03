import type { token, tokenRequest } from 'models/auth/token'
import type { userResponse } from 'models/user/userResponse'
import Api from '@/utils/Api/Api'
import { jwtDecode } from 'jwt-decode'

export default class auth {
  private api: Api = new Api()

  constructor(api?: Api) {
    if (api) this.api = api
  }

  public async login(data: Record<string, any>): Promise<boolean> {
    try {
      const response: userResponse = (await this.api.post('auth/login', data)) as userResponse
      if (response && response?.status === 200) {
        if (response.token === undefined) {
          throw response
        }
        this.setRefreshToken(response.token.refresh)
        this.setAccessToken(response.token.access)
        this.setAuthHeader()
        return true
      } else {
        console.error('Error in login:', response)
        window.alert('An error occurred while submitting the form login')
        return false
      }
    } catch (error: any) {
      console.error('Error logging in:', error)
      return false
    }
  }

  public async logout(): Promise<boolean> {
    try {
      const response = await this.api.post<Record<string, any>>(
        'auth/logout',
        {
          token: localStorage.getItem('refresh_token') as string
        },
        ['status'],
        {
          Authorization: `Bearer ${localStorage.getItem('access_token') as string}`
        }
      )

      if (response && response?.status === 200) {
        this.removeAccessToken()
        return true
      } else {
        console.error('Error logging out:', response)
        return false
      }
    } catch (error: any) {
      console.error('Error logging out:', error)
      return false
    }
  }

  public async register(data: Record<string, any>): Promise<boolean> {
    try {
      const response = (await this.api.post<userResponse>('auth/register', data)) as userResponse
      if (response.status === 201) {
        const userId = response.id
        const userDataArray = [userId, data.nickname]
        this.crtPongTable(userDataArray)
        return true
      } else {
        throw response.code
      }
    } catch (error: any) {
      const response = error
      switch (response) {
        case 'user_exists':
          console.log('Username is not available. Try again with a different one.')
          alert('Username is not available. Try again with a different one or log in.')
          return true

        case 'nickname_exists':
          console.log('Nickname is not available. Try again with a different one.')
          alert('Nickname is not available. Try again with a different one.')
          return false

        case 'email_exists':
          console.log('Email is not available. Try again with a different one.')
          alert('Email is not available. Try again with a different one.')
          return false

        case 'token_not_valid':
          console.log('Token invalid. Redirecting to login.')
          this.removeAccessToken()
          return false

        default:
          console.error('Unexpected token status:', response)
          this.removeAccessToken()
          return false
      }
    }
  }

  public async crtPongTable(data: Record<string, any>): Promise<any> {
    try {
      const response = await this.api.post<userResponse>('pong/register/' + data[0] + '/', {
        id: data[0],
        name: data[1]
      })
      if (response.status === 200) {
        return true
      }
    } catch (error: any) {
      console.error('Error registering pong data:', error)
      return false
    }
  }

  public async whoami(): Promise<any> {
    try {
      const response = await this.api.get('auth/whoami')

      if (response && response?.status === 200) {
        return response
      } else {
        console.error('Error getting username:', response)
        return false
      }
    } catch (error: any) {
      console.error('Error getting username:', error)
      return false
    }
  }

  public async pongData(id: number): Promise<any> {
    try {
      //const response = await this.api.get('pong/user/' + id + '/')
      const response = await this.api.get('pong/user/' + id + '/')

      if (response && response?.status === 200) {
        return response
      } else {
        console.error('Error getting username:', response)
        return false
      }
    } catch (error: any) {
      console.error('Error getting username:', error)
      return false
    }
  }

  public async checkAndRefreshToken(): Promise<any> {
    try {
      const accessToken = localStorage.getItem('access_token')
      if (accessToken) {
        if (this.isTokenValid(accessToken) == false) {
          console.log('Token expired. Attempting to refresh.')
          return await this.refreshAuthToken()
        } else {
          this.setAuthHeader()
          const response: any = await this.api.post<tokenRequest>('auth/token/verify', {
            token: accessToken as string
          })

          if (response.status === 200) {
            return true // Token is still valid
          } else {
            throw response
          }
        }
      }
    } catch (error) {
      const response = error as token
      switch (response.code) {
        case 'expired':
          console.log('Token expired. Attempting to refresh.')
          console.log(await this.refreshAuthToken())
          return true

        case 'token_not_valid':
          console.log('Token invalid. Redirecting to login.')
          this.removeAccessToken()
          return false

        case 'missing':
          console.log('Token missing. Redirecting to login.')
          this.removeAccessToken()
          return false

        default:
          console.error('Unexpected token status:')
          this.removeAccessToken()
          return false
      }
    }
  }

  public isTokenValid(token: any) {
    if (!token) return false
    try {
      const decoded = jwtDecode(token)
      const currentTime = Date.now() / 1000 // tiempo actual en segundos
      // Verifica si el token ha expirado
      if (decoded.exp && decoded.exp < currentTime) {
        return false // Token ha expirado
      }
      return true // Token es válido
    } catch (error) {
      console.error('Error decodificando el token:', error)
      return false
    }
  }

  public async refreshAuthToken() {
    try {
      const refreshToken = localStorage.getItem('refresh_token')
      const response = (await this.api.post('auth/token/refresh', {
        refresh: refreshToken
      })) as token
      if (response.status === 200) {
        const newAccessToken = response.access
        const newRefreshToken = response.refresh
        this.setAccessToken(newAccessToken)
        this.setRefreshToken(newRefreshToken)
        return true
      } else throw response
    } catch (error) {
      const response = error as token
      switch (response.code) {
        case 'expired':
          console.log('Token expired. Removed tokens...')
          this.removeAccessToken()
          return false

        case 'token_not_valid':
          console.log('Token invalid. Redirecting to login.')
          this.removeAccessToken()
          return false

        case 'missing':
          console.log('Token missing. Redirecting to login.')
          this.removeAccessToken()
          return false

        default:
          console.error('Unexpected token status:')
          this.removeAccessToken()
          return false
      }
    }
  }

  public setAuthHeader() {
    const accessToken = localStorage.getItem('access_token')
    if (accessToken) {
      this.api.setAccessToken(accessToken)
    }
  }

  public setAccessToken(accessToken: any) {
    localStorage.setItem('access_token', accessToken)
    this.setAuthHeader() // Update headers with the new token
  }

  public setRefreshToken(refreshToken: any) {
    localStorage.setItem('refresh_token', refreshToken)
  }

  public removeAccessToken() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    this.api.removeAccessToken()
  }
}
