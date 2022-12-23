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

  static async getSpecialists(page, pageSize, orderValue, position, date) {
    const argParams = {
      page: page,
      page_size: pageSize,
      position: position,
      ordering: orderValue,
      date: date,
    };
    const filteredParams = Object.fromEntries(Object.entries(argParams).filter(([key, value]) => !!value));

    const response = await this.api.get('/specialists/', {
      params: filteredParams,
    });
    return response;
  };

  static async getSpecialist(id) {
    const response = await this.api.get(`/specialists/${id}`);
    return response;
  };

  static async getSpecialistFreeTime(id, date) {
    const response = await this.api.get(`/specialists/${id}/schedule/${date}`);
    return response;
  };
}
