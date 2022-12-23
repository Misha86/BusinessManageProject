import { useMemo } from 'react';

const useStringDate = (dateData) => {
  const stringDate = useMemo(() => {
    return dateData ? `${dateData?.get('y')}-${dateData?.get('M') + 1}-${dateData?.get('D')}` : '';
  }, [dateData]);

  return stringDate;
};

export default useStringDate;
