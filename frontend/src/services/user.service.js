import axios from 'axios';

export default class UserService {
  static api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
  });

  static getUser() {
    const auth = JSON.parse(localStorage.getItem('auth'));
    return auth?.user;
  }

  static getUserGroups() {
    const auth = JSON.parse(localStorage.getItem('auth'));
    return auth?.user.groups;
  }

  static async getSpecialists() {
    const response = await this.api.get('/specialists/');
    return response;
  }
}
