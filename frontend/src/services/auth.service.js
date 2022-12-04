import axios from 'axios';

export default class AuthService {
  static api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
  });

  static async login(userData) {
    const response = await this.api.post('http://localhost:8000/api/token/', userData);
    this.setAuthData(response.data);
    return response;
  }

  static async logOut(access_token, refresh_token) {
    const response = await this.api.post(
      'http://localhost:8000/api/token/logout/',
      { refresh: refresh_token },
      {
        headers: {
          Authorization: `JWT ${access_token}`,
        },
      }
    );
    this.removeAuthData();
    return response;
  }

  static getAuthData() {
    return JSON.parse(localStorage.getItem('auth'));
  }

  static setAuthData(data) {
    return localStorage.setItem('auth', JSON.stringify(data));
  }

  static removeAuthData() {
    return localStorage.removeItem('auth');
  }
}
