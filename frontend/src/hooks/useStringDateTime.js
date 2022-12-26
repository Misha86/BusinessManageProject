import { useMemo } from 'react';

const useStringDateTime = (dateTimeData) => {
  const stringDateTime = useMemo(() => {
    const year = dateTimeData?.get('y');
    const month = dateTimeData?.get('M') + 1;
    const date = dateTimeData?.get('D');
    const hours = dateTimeData?.get('h');
    const minutes = dateTimeData?.get('m');
    return dateTimeData
      ? `${year}-${month}-${date}T${hours}:${minutes.toString().length === 1 ? '0' + minutes : minutes}:00`
      : '';
  }, [dateTimeData]);

  return stringDateTime;
};

export default useStringDateTime;
