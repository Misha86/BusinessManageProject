import { useContext, useEffect, useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import { AuthContext } from '../context';
import { publicRoutes, ManagerRoutes, AdminRoutes } from '../router/router';

const AppRouter = () => {
  const { auth } =useContext(AuthContext)
  const {isAuth, user, ...rest} = auth
  const [routers, setRouters] = useState([])
   useEffect(() => {
      if (isAuth && user.groups.includes("Manager")) {
        setRouters(ManagerRoutes)
      } else if (isAuth && user.groups.includes("Admin")) { 
        setRouters(AdminRoutes)
      } else{
        setRouters(publicRoutes)
      }
   }, [auth])

  return (
    <Routes>
      {routers.map((router) => (
        <Route
          path={router.path}
          element={<router.component />}
          exact={router.exact}
          key={router.path}
        />
      ))}
    </Routes>
  );
};

export default AppRouter;
