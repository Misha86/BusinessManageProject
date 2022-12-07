export const getEmptySchedule = (days) => {
    return days.reduce((accumulator, value) => {
      return { ...accumulator, [value]: [] };
    }, {});
  };