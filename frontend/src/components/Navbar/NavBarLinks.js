export const loginLinks = [{ title: 'Login', sx: { marginLeft: 'auto' }, to: '/login' }];

const logoutLinks = [{ title: 'Logout', sx: { marginLeft: 'auto'} }];

export const managerLinks = [
  { title: 'Add Specialist', to: '/add-specialist' },
  { title: 'Add Schedule', to: '/add-schedule' },
  { title: 'Add Location', to: '/add-location' },
  ...logoutLinks,
];

export const adminLinks = [
  { title: 'Create Appointment', to: '/add-appointment' },
  ...logoutLinks,
];
