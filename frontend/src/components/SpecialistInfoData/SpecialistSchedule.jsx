import React from 'react';
import { Grid, Typography } from '@mui/material';

const SpecialistSchedule = ({ specialist }) => {
  return (
    <>
      {specialist.schedule?.working_time &&
        Object.entries(specialist.schedule?.working_time).map(([day, intervals]) => (
          <Grid item key={day}>
            <Typography variant="subtitle1" component="p" sx={{ textAlign: 'justify' }}>
              <b>{day}: </b>
              {intervals.length ? intervals.map((interval) => `${interval.join('-')} `) : <em>Day Off</em>}
            </Typography>
          </Grid>
        ))}
    </>
  );
};

export default SpecialistSchedule;
