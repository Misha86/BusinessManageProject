import instance from './api';

export class AuthService {

  static async login(userData) {
    const response = await instance.post('/token/', userData);
    this.setAuthData(response.data);
    return response;
  };

  static getLoginFieldsOption() {
    const response = instance.options('/token/')
    return response;
  }

  static async logOut(refresh_token) {
    const response = await instance.post('/token/logout/', { refresh: refresh_token });
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

  static addSpecialist(specialistData) {
    const response = instance.post(
      '/specialists/',
      { ...specialistData },
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response;
  };

  static addLocation(locationData) {
    const response = instance.post(
      '/locations/',
      { ...locationData },
      {
        headers: {
          'Content-Type':  'application/json',
        },
      }
    );
    return response;
  };

  static addSchedule(scheduleData) {
    const response = instance.post(
      '/schedules/',
      { ...scheduleData },
      {
        headers: {
          'Content-Type':  'application/json',
        },
      }
    );
    return response;
  };

  static async getSpecialistFieldsOption() {
    const response = await instance.options('/specialists/')
    return response;
  };

  static getLocationFieldsOption() {
    const response = instance.options('/locations/')
    return response;
  };

  static getScheduleFieldsOption() {
    const response = instance.options('/schedules/')
    return response;
  };
}

export class AdminService {

  static async appointmentFieldsOption() {
    const response = await instance.options('/appointments/')
    return response;
  };

  static addAppointment(appointmentData) {
    const response = instance.post(
      '/appointments/',
      { ...appointmentData },
      {
        headers: {
          'Content-Type':  'application/json',
        },
      }
    );
    return response;
  };

}

