import Home from "../pages/Home";
import AddSpecialist from '../pages/AddSpecialist';
import AddSchedule from '../pages/AddSchedule';
import NoPage from "../pages/NoPage";
import AddLocation from '../pages/AddLocation';
import Login from '../pages/Login';


export const publicRoutes = [
  { path: '/', component: Home, exact: true },
  { path: '/add-specialist', component: AddSpecialist, exact: true },
  { path: '/add-schedule', component: AddSchedule, exact: true },
  { path: '/add-location', component: AddLocation, exact: true },
  { path: '/login', component: Login, exact: true },
  { path: '*', component: NoPage },
];
