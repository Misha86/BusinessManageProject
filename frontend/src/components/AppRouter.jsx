import { useContext, useEffect, useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import { AuthContext } from '../context';
import { publicRoutes, ManagerRoutes, AdminRoutes } from '../router/router';
import UserService from '../services/user.service';

const AppRouter = () => {
  const { auth } = useContext(AuthContext);
  const [routers, setRouters] = useState([]);

  useEffect(() => {
    const roles = UserService.getUserGroups();
    if (roles && roles.includes('Manager')) {
      setRouters(ManagerRoutes);
    } else if (roles && roles.includes('Admin')) {
      setRouters(AdminRoutes);
    } else {
      setRouters(publicRoutes);
    }
  }, [auth]);

  return (
    <Routes>
      {routers.map((router) => (
        <Route path={router.path} element={<router.component />} exact={router.exact} key={router.path} />
      ))}
    </Routes>
  );
};

export default AppRouter;
