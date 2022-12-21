import Home from "../pages/Home";
import AddSpecialist from '../pages/AddSpecialist';
import AddSchedule from '../pages/AddSchedule';
import NoPage from "../pages/NoPage";
import AddLocation from '../pages/AddLocation';
import AddAppointment from '../pages/AddAppointment';
import SpecialistInfo from '../pages/SpecialistInfo';
import Login from '../pages/Login';


export const baseRoutes = [
  { path: '/', component: Home, exact: true },
  { path: '/specialists/:id', component: SpecialistInfo, exact: true },
  { path: '*', component: NoPage },
];


export const publicRoutes = [
  ...baseRoutes,
  { path: '/login', component: Login, exact: true },
];


export const AdminRoutes = [
  ...baseRoutes,
  { path: '/add-appointment', component: AddAppointment, exact: true },
];

export const ManagerRoutes = [
  ...baseRoutes,
  { path: '/add-specialist', component: AddSpecialist, exact: true },
  { path: '/add-schedule', component: AddSchedule, exact: true },
  { path: '/add-location', component: AddLocation, exact: true },
];