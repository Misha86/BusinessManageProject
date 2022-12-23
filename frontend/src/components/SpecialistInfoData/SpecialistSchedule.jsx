import React, { useMemo } from 'react';
import { Grid, Typography } from '@mui/material';

const SpecialistSchedule = ({ specialist }) => {
  const workingDays = useMemo(() => {
    if (specialist.schedule) {
      const daysIntervals = Object.entries(specialist.schedule?.working_time).filter(
        ([day, intervals]) => !!intervals.length
      );
      return daysIntervals.length ? daysIntervals : null;
    }
  }, [specialist]);

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
