import axios from 'axios';


export default class UserService {
  static api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
  });

  static async login(userData) {
    const response = await this.api.post('http://localhost:8000/api/token/', userData);
    localStorage.setItem('token', JSON.stringify(response.data.access));
  }
}
