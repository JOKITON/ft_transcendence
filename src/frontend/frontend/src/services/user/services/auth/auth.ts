import type { token, tokenRequest } from '@/models/auth/token'
import type { userResponse } from '@/models/user/userResponse'
import type { ApiResponse } from '@/utils/Api/IApi'
import Api from '../../../../utils/Api/Api'
import type IAuth from './IAuth'
import axios from 'axios'

export default class auth implements IAuth {
  private api: Api = new Api()

  constructor(api?: Api) {
    if (api) this.api = api
  }

  public async login(data: Record<string, any>): Promise<boolean> {
    try {
      const response: ApiResponse<userResponse> = await this.api.post<userResponse>('auth/login', data)
      if (response && response?.status === 200) {
        this.setRefreshToken(response.token.refresh);
        this.setAccessToken(response.token.access)
        this.setAuthHeader();
        return true
      } else {
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
      const response: ApiResponse<Record<string, any>> = await this.api.post<Record<string, any>>(
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
        this.removeToken()
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
      const response: ApiResponse<userResponse> = await this.api.post<userResponse>(
        'register',
        data
      )
      if (response.status === 200) {
        return true
      } else {
        console.error('error de registro')
        return false
      }
    } catch (error: any) {
      console.error('Error registering user:', error)
      return false
    }
  }

  public async checkAndRefreshToken(): Promise<boolean> {
    try {
      const accessToken = localStorage.getItem('access_token');
      if (accessToken) {
        this.setAuthHeader();
        const response: ApiResponse<tokenRequest> = await this.api.post<tokenRequest>(
        'auth/token/verify',
        {
          token: accessToken as string
        });
  
        if (response.status === 200) {
          return true; // Token is still valid
        }
      }
      else
        console.log('No token found. Redirecting to login.');
        return false;
    } catch (error) {
      const response = error.response;
      switch (response.data.code) {
        case 'expired':
          console.log('Token expired. Attempting to refresh.');
          return (await this.refreshAuthToken());
  
        case 'token_not_valid':
          console.log('Token invalid. Redirecting to login.');
          this.removeAccessToken();
          return false;
  
        case 'missing':
          console.log('Token missing. Redirecting to login.');
          this.removeAccessToken();
          return false;
  
        default:
          console.error('Unexpected token status:', response.data.status);
          this.removeAccessToken();
          return false;
      }
    }
  }

  public async refreshAuthToken() {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      const response: ApiResponse<tokenRequest> = await this.api.post<tokenRequest>(
        'token/refresh',
        {
          token: refreshToken
        });

      const newAccessToken = response.data.access;
      const newRefreshToken = response.data.refresh;
      if (newAccessToken) {
        this.setAccessToken(newAccessToken);
      }
      if (newRefreshToken)
        this.setRefreshToken(newRefreshToken);

      return true;
    } catch (error) {
      console.error(
        "Refresh token error:",
        error.response ? error.response.data : error.message
      );
      alert("Session expired. Please log in again.");
      return false;
    }
  }

  public setAuthHeader() {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
      this.api.setAccessToken(accessToken);
    }
  }

  public setAccessToken(accessToken) {
    localStorage.setItem('access_token', accessToken);
    this.setAuthHeader(); // Update headers with the new token
  }
  
  public setRefreshToken(refreshToken) {
    localStorage.setItem('refresh_token', refreshToken);
  }
  
  public removeAccessToken() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.api.removeAccessToken();
  }
}
