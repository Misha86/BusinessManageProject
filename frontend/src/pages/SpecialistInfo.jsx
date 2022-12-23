import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import useFetching from '../hooks/useFetching';
import useWorkingDays from '../hooks/useWorkingDays';
import useStringDate from '../hooks/useStringDate';
import UserService from '../services/user.service';
import Loader from '../components/Loader';
import { Container, Grid } from '@mui/material';
import SpecialistInfoData from '../components/SpecialistInfoData/SpecialistInfoData';
import { useNavigate } from 'react-router-dom';
import CalendarField from '../components/UI/CalendarField';
import ErrorDetail from '../components/Form/ErrorDetail';
import TimeIntervals from '../components/TimeIntervals';


const SpecialistInfo = () => {
  const { id } = useParams();
  const router = useNavigate();

  const [specialist, setSpecialist] = useState({});
  const [freeTime, setFreeTime] = useState(null);
  const [dateData, setDateData] = useState(null);

  const workingDays = useWorkingDays(specialist)
  const stringDate = useStringDate(dateData);
  const [fetching, isLoading, error] = useFetching(async (id) => {
    const response = await UserService.getSpecialist(id);
    setSpecialist(response.data);
  });

  const [fetchingFreeTime, _, errorFreeTime] = useFetching(async (id, date) => {
    setFreeTime(null);
    const response = await UserService.getSpecialistFreeTime(id, date);
    setFreeTime(response.data.free_intervals);
  });

  useEffect(() => {
    fetching(id);
  }, []);

  useEffect(() => {
    fetchingFreeTime(id, stringDate);
  }, [dateData]);

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
            <Grid container item>
              <Grid item>
                <ErrorDetail error={errorFreeTime} />
              </Grid>
              <Grid container item spacing={2}>
                {(specialist?.schedule && workingDays) && (
                  <Grid item>
                    <CalendarField setDateData={setDateData} dateData={dateData} label="Check free time" />
                  </Grid>
                )}

                {freeTime && (
                  <Grid item>
                    <TimeIntervals freeTime={freeTime} />
                  </Grid>
                )}
              </Grid>
            </Grid>
          </Grid>
        </Container>
      )}
    </>
  );
};

export default SpecialistInfo;
