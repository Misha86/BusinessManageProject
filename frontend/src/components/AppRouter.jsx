import { Route, Routes } from 'react-router-dom';
import { publicRoutes } from '../router/router';

const AppRouter = () => {
  return (
    <Routes>
      {publicRoutes.map((router) => (
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
