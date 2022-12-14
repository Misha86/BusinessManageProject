import axios from 'axios';
import TokenService from './token.service';
import { AuthService } from './auth.service';

const instance = axios.create({
  baseURL: 'http://localhost:8000/api',
  // headers: {
  //   "Content-Type": "application/json",
  // },
});

instance.interceptors.request.use(
  (config) => {
    const token = TokenService.getAccessToken();
    if (token) {
      config.headers['Authorization'] = `JWT ${token}`; // for Spring Boot back-end
    }
    if (config.method === 'post') {
      config.headers['X-CSRFToken'] = TokenService.getCsrfToken();
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

instance.interceptors.response.use(
  (res) => {
    return res;
  },
  async (err) => {
    const originalConfig = err.config;
    // Refresh Token was expired
    if (err.response.status === 401 && originalConfig.url === '/token/refresh/') {
      AuthService.removeAuthData();
      window.location.href = '/login';
      return Promise.reject();
    }
    if (originalConfig.url !== '/token/' && err.response) {
      // Access Token was expired
      if (err.response.status === 401 && !originalConfig._retry) {
        originalConfig._retry = true;

        try {
          const response = await instance.post('/token/refresh/', {
            refresh: TokenService.getRefreshToken(),
          });

          const { access } = response.data;
          TokenService.updateAccessToken(access);

          return instance(originalConfig);
        } catch (_error) {
          return Promise.reject(_error);
        }
      }
    }

    return Promise.reject(err);
  }
);

export default instance;
