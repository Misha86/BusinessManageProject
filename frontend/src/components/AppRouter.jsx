import { useContext, useEffect, useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import { AuthContext } from '../context';
import { publicRoutes, ManagerRoutes, AdminRoutes } from '../router/router';

const AppRouter = () => {
  const { isAuth, auth, isLoading } =useContext(AuthContext)
  const [routers, setRouters] = useState([])
   useEffect(() => {
      if (isAuth && auth.groups.includes("Manager")) {
        setRouters(ManagerRoutes)
      } else if (isAuth && auth.groups.includes("Admin")) {
        setRouters(AdminRoutes)
      } else{
        setRouters(publicRoutes)
      }
   }, [isAuth, auth])

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
