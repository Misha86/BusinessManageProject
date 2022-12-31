export const getEmptySchedule = (days) => {
  return days.reduce((accumulator, value) => {
    return { ...accumulator, [value]: [] };
  }, {});
};

export const messageTimeout = (time, messageState) => {
  setTimeout(() => {
    messageState(false);
  }, time);
};

export const weekDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

export const pageSizeOptions = [
  [10, 10],
  [20, 20],
  [30, 30],
  [50, 50],
];

export const sortOptions = [
  ['email', 'Email'],
  ['position', 'Position'],
  ['first_name', 'Name'],
];

export const positionsOptions = [
  { label: 'Position 1', position: 'position_1' },
  { label: 'Position 2', position: 'position_2' },
  { label: 'Position 3', position: 'position_3' },
  { label: 'Position 4', position: 'position_4' },
];
