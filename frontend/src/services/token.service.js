export default class TokenService {

  static getRefreshToken(){
    const auth = JSON.parse(localStorage.getItem('auth'));
    return auth?.refresh;
  };
  
  static getAccessToken(){
    const auth = JSON.parse(localStorage.getItem('auth'));
    return auth?.access;
  };

  static updateAccessToken(token){
    let auth = JSON.parse(localStorage.getItem('auth'));
    auth.access = token;
    localStorage.setItem('auth', JSON.stringify(auth));
  };
}
