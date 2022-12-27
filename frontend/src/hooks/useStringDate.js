import { useMemo, useState } from 'react';

const useStringDate = (dateData) => {
  const [savedDate, setSavedDate] = useState(null);
  let validDate;

  if (!dateData || dateData?.isValid()) {
    validDate = dateData;
  }
  if (validDate === undefined) {
    validDate = savedDate;
  }

  const stringDate = useMemo(() => {
    if (validDate) {
      const year = dateData.get('y');
      const month = dateData?.get('M') + 1;
      const date = dateData?.get('D');
      setSavedDate(dateData);
      return dateData ? `${year}-${month}-${date}` : null;
    }
  }, [validDate]);

  return stringDate;
};

export default useStringDate;
