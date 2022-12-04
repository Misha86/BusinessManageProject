export default class UserService {
  static getUser() {
    const auth = JSON.parse(localStorage.getItem('auth'));
    return auth?.user;
  }
  static getUserGroups() {
    const auth = JSON.parse(localStorage.getItem('auth'));
    return auth?.user.groups;
  }
}
