import axios from 'axios';

export default class UserService {
  static api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
  });

  static async login(userData) {
    const response = await this.api.post('http://localhost:8000/api/token/', userData);
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
    return response;
  }
}
