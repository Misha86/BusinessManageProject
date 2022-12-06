export default class TokenService {
  static getRefreshToken() {
    const auth = JSON.parse(localStorage.getItem('auth'));
    return auth?.refresh;
  }

  static getAccessToken() {
    const auth = JSON.parse(localStorage.getItem('auth'));
    return auth?.access;
  }

  static updateAccessToken(token) {
    let auth = JSON.parse(localStorage.getItem('auth'));
    auth.access = token;
    localStorage.setItem('auth', JSON.stringify(auth));
  }

  static getCsrfToken() {
    const cookieName = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, cookieName.length + 1) === cookieName + '=') {
          cookieValue = decodeURIComponent(cookie.substring(cookieName.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
}
