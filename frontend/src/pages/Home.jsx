import React, { useState, useEffect } from 'react';
import UserService from '../services/user.service';
import useFetching from '../hooks/useFetching';
import Loader from '../components/Loader';
import SpecialistList from '../components/SpecialistList';

const Home = () => {
  const [specialists, setSpecialists] = useState([]);
  const [fetching, isLoading] = useFetching(async () => {
    const response = await UserService.getSpecialists();
    setSpecialists(response.data.results);
  });

  useEffect(() => {
    fetching();
  }, []);

  return <>{isLoading ? <Loader /> : <SpecialistList specialists={specialists} />}</>;
};

export default Home;
