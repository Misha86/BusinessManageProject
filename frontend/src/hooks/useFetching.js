import { useState } from 'react';

const useFetching = (callback) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState({});

  const fetching = async () => {
    try {
      setIsLoading(true);
      await callback();
      setError({});
    } catch (error) {
      console.log(error.response);
      setError(error.response?.data);
    } finally {
      setIsLoading(false);
    }
  };

  return [fetching, isLoading, error];
};

export default useFetching;
