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

  static async getSpecialists(page=1, pageSize=0, orderValue='', position='') {
    const response = await this.api.get('/specialists/', {
      params: { page: page, page_size: pageSize, position: position, ordering: orderValue },
    });
    return response;
  }
}
