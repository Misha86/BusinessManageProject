import React from 'react';
import { Grid, Typography } from '@mui/material';

const TimeIntervals = ({ freeTime }) => {
  return (
    <>
      <Grid container item direction="column" mt={2}>
        <Typography variant="subtitle1" component="p">
          <b>Free time: </b>
        </Typography>
        {freeTime.map((interval, index) => (
          <Typography key={index} variant="subtitle1" component="p">
            {interval.join('-')}
          </Typography>
        ))}
      </Grid>
    </>
  );
};

export default TimeIntervals;
