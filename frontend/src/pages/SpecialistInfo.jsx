import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import useFetching from '../hooks/useFetching';
import UserService from '../services/user.service';
import Loader from '../components/Loader';
import { Container, Grid } from '@mui/material';
import SpecialistInfoData from '../components/SpecialistInfoData/SpecialistInfoData';
import { useNavigate } from 'react-router-dom';
import CalendarField from '../components/UI/CalendarField';

const SpecialistInfo = () => {
  const { id } = useParams();
  const router = useNavigate();

  const [specialist, setSpecialist] = useState({});
  const [dateData, setDateData] = useState(null);

  const [fetching, isLoading, error] = useFetching(async (id) => {
    const response = await UserService.getSpecialist(id);
    setSpecialist(response.data);
  });

  useEffect(() => {
    fetching(id);
  }, []);

  useEffect(() => {
    if (error) {
      router('/');
    }
  }, [error]);

  return (
    <>
      {isLoading ? (
        <Loader />
      ) : (
        <Container maxWidth="xl">
          <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
            <SpecialistInfoData specialist={specialist} />
            <Grid item xs={6} sm={4} md={3} mb={2} >
              <CalendarField setDateData={setDateData} dateData={dateData} label="Check free time" />
            </Grid>
          </Grid>
        </Container>
      )}
    </>
  );
};

export default SpecialistInfo;
