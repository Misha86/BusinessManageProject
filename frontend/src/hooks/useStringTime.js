import { useMemo } from 'react';

const useStringTime = (timeData) => {
  const stringTime = useMemo(() => {
    const hours = timeData?.get('h');
    const minutes = timeData?.get('m');
    return timeData
      ? `${hours}:${minutes.toString().length === 1 ? '0' + minutes : minutes}:00`
      : '';
  }, [timeData]);

  return stringTime;
};

export default useStringTime;
  