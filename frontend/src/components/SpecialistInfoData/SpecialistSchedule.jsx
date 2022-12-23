import React from 'react';
import { Grid, Typography } from '@mui/material';
import useWorkingDays from '../../hooks/useWorkingDays';

const SpecialistSchedule = ({ specialist }) => {
  const workingDays = useWorkingDays(specialist)

  return (
    <Grid item container direction="column">
      <Grid item>
        <Typography variant="subtitle1" component="p">
          <b>SCHEDULE: </b>
          {!workingDays && 'No working days'}
        </Typography>
      </Grid>
      
      {workingDays &&
        workingDays.map(([day, intervals]) => (
          <Grid item key={day}>
            <Typography variant="subtitle1" component="p" sx={{ textAlign: 'justify' }}>
              <b>{day}: </b>
              {intervals.length ? intervals.map((interval) => `${interval.join('-')} `) : <em>Day Off</em>}
            </Typography>
          </Grid>
        ))}
    </Grid> 
  );
};

export default SpecialistSchedule;
