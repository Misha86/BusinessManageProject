import { useMemo } from 'react';

const useStringDateTime = (dateTimeData) => {
  const year = dateTimeData?.get('y');
  const month = dateTimeData?.get('M') + 1;
  const date = dateTimeData?.get('D');
  const hours = dateTimeData?.get('h');
  const minutes = dateTimeData?.get('m');

  const stringDateTime = useMemo(() => {
    return dateTimeData
      ? `${year}-${month}-${date}T${hours}:${minutes.toString().length === 1 ? '0' + minutes : minutes}:00`
      : '';
  }, [dateTimeData]);

  return stringDateTime;
};

export default useStringDateTime;
