import instance from './api';

export class AuthService {
  static api = instance;

  static async login(userData) {
    const response = await this.api.post('/token/', userData);
    this.setAuthData(response.data);
    return response;
  }

  static async logOut(refresh_token) {
    const response = await this.api.post('/token/logout/', { refresh: refresh_token });
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

export class ManagerService {
  static api = instance;

  static addSpecialist(specialistData) {
    const response = this.api.post(
      '/specialists/',
      { ...specialistData },
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          // 'X-CSRFTOKEN': CSRF_TOKEN
        },
      }
    );
    return response;
  }
}
