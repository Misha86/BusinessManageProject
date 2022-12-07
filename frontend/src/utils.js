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
