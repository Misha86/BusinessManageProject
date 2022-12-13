import { useState, useEffect } from 'react';

const useOptions = (optionsService) => {
  const [optionsData, setOptionsData] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const getFieldsInfo = async () => {
      await optionsService()
        .then((response) => {
          setOptionsData(response.data.fields);
        })
        .catch((error) => {
          console.log(error.response.data);
        });
    };
    getFieldsInfo();
    setIsLoading(false);
  }, [optionsService]);

  return [optionsData, setOptionsData, isLoading, setIsLoading];
};

export default useOptions;
