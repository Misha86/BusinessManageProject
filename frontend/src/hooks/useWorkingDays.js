import { useMemo } from 'react';

const useWorkingDays = (specialist) => {
  const workingDays = useMemo(() => {
    if (specialist?.schedule) {
      const daysIntervals = Object.entries(specialist.schedule?.working_time).filter(
        ([day, intervals]) => !!intervals.length
      );
      return daysIntervals.length ? daysIntervals : null;
    }
  }, [specialist]);

  return workingDays;
};

export default useWorkingDays;
