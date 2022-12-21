import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import useFetching from '../hooks/useFetching';
import UserService from '../services/user.service';
import Loader from '../components/Loader';
import { Grid, Container, Typography, Paper } from '@mui/material';
import { Image } from 'mui-image';

const SpecialistInfo = () => {
  const { id } = useParams();
  const [specialist, setSpecialist] = useState({});
  const [fetching, isLoading, error] = useFetching(async (id) => {
    const response = await UserService.getSpecialist(id);
    setSpecialist(response.data);
  });

  const fullName = `${specialist.first_name} ${specialist.last_name}`;

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
          <Grid container rowSpacing={2} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
            <Grid item xs display="flex" mt={1} justifyContent="center" alignItems="center">
              <Typography gutterBottom variant="h5" component="h5" color="gray">
                {fullName}
              </Typography>
            </Grid>

            <Grid container item spacing={3}>
              <Grid item xs={6} sm={5} md={5}>
                <Paper elevation={3}>
                  <Image src={specialist.avatar} alt={fullName} showLoading shift="top" distance={300} />
                </Paper>
              </Grid>

              <Grid container item xs={12} spacing={2} sm={7} md={7} direction="column">
                <Grid item>
                  <Typography variant="subtitle1" component="p">
                    <b>POSITION: </b>
                    {`${specialist.position}`.toUpperCase()}
                  </Typography>
                </Grid>
                <Grid item>
                  <Typography variant="subtitle1" component="p" sx={{ textAlign: 'justify' }}>
                    <b>BIO: </b>
                    {specialist.bio}
                  </Typography>
                </Grid>
                <Grid item container direction="column">
                  <Grid item>
                    <Typography variant="subtitle1" component="p">
                      <b>SCHEDULE: </b>
                    </Typography>
                  </Grid>
                  {specialist.schedule?.working_time &&
                    Object.entries(specialist.schedule?.working_time).map(([day, intervals]) => (
                      <Grid item key={day}>
                        <Typography variant="subtitle1" component="p" sx={{ textAlign: 'justify' }}>
                          <b>{day}: </b>{' '}
                          {intervals.length ? intervals.map((interval) => `${interval.join('-')} `) : <em>Day Off</em>}
                        </Typography>
                      </Grid>
                    ))}
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Container>
      )}
    </>
  );
};

export default SpecialistInfo;
