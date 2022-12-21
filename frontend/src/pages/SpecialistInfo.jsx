import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import useFetching from '../hooks/useFetching';
import UserService from '../services/user.service';
import Loader from '../components/Loader';
import { Container } from '@mui/material';
import SpecialistInfoData from '../components/SpecialistInfoData/SpecialistInfoData';

const SpecialistInfo = () => {
  const { id } = useParams();
  const [specialist, setSpecialist] = useState({});
  const [fetching, isLoading, error] = useFetching(async (id) => {
    const response = await UserService.getSpecialist(id);
    setSpecialist(response.data);
  });

  useEffect(() => {
    fetching(id);
  }, []);

  useEffect(() => {
    if (error) {
      window.location.replace('/');
    }
  }, [error]);

  return (
    <>
      {isLoading ? (
        <Loader />
      ) : (
        <Container maxWidth="xl">
          <SpecialistInfoData specialist={specialist} />
        </Container>
      )}
    </>
  );
};

export default SpecialistInfo;
