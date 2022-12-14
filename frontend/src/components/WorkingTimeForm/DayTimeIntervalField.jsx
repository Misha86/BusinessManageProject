import React, { useEffect, useState, useContext } from 'react';
import { InputLabel, Typography, Grid, Icon, IconButton } from '@mui/material';
import TimeIntervalField from './TimeIntervalField';
import { PaperStyled } from '../styles/Paper.styled';
import { WorkingFormContext } from '../../context';

const DayTimeIntervalField = ({ weekDay, fieldTitle, error, handler }) => {
  const errorMessage = error[fieldTitle]?.[weekDay];
  const [intervals, setIntervals] = useState([]);
  const { countOfTimeIntervals } = useContext(WorkingFormContext);

  const removeInterval = (intervals, setIntervals) => {
    if (intervals.length >= 1) {
      intervals.pop();
      setIntervals([...intervals]);
    }
  };

  const addInterval = (intervals, setIntervals, count) => {
    if (intervals.length < count) {
      setIntervals([...intervals, []]);
    }
  };

  const status = localStorage.getItem('created', 'true');

  useEffect(() => {
    const timeIntervals = intervals.filter((interval) => interval.length > 0);
    const dayTimeIntervals = { [weekDay]: countOfTimeIntervals > 1 ? timeIntervals : timeIntervals[0] };
    handler(dayTimeIntervals);
    status === 'true' && setIntervals([]);
    localStorage.removeItem('created');
  }, [intervals, status]);

  return (
    <Grid container spacing={1}>
      {!!errorMessage && (
        <Grid item xs={12} md={12}>
          <Typography component="p" variant="p" color="error">
            {errorMessage}
          </Typography>
        </Grid>
      )}

      <Grid justifyContent="flex-end" item xs={4} md={2}>
        <Grid item xs={12} md={12}>
          <InputLabel error={!!errorMessage}>{weekDay}</InputLabel>
        </Grid>

        {intervals.length < countOfTimeIntervals && (
          <Grid item xs={12} md={12} padding="none">
            <IconButton
              sx={{ padding: 0 }}
              aria-label="add time interval"
              onClick={() => addInterval(intervals, setIntervals, countOfTimeIntervals)}
            >
              <Icon color="primary">add_circle</Icon>
            </IconButton>
          </Grid>
        )}

        {intervals.length >= 1 && (
          <Grid item xs={12} md={12}>
            <IconButton
              sx={{ padding: 0 }}
              aria-label="remove time interval"
              onClick={() => removeInterval(intervals, setIntervals)}
            >
              <Icon color="primary">do_not_disturb_on</Icon>
            </IconButton>
          </Grid>
        )}
      </Grid>
      
      <Grid container item xs={8} md={10}>
        {intervals.length === 0 && (
          <Grid item mt={3}>
            <Typography component="p" variant="p">
              {`Add working interval for ${weekDay}`}
            </Typography>
          </Grid>
        )}

        {intervals.map((_, intervalIndex) => (
          <Grid container item spacing={1} mb={1} key={intervalIndex}>
            {['Start time', 'End time'].map((title, timeIndex) => (
              <Grid item xs={12} md={6} key={`${intervalIndex}-${timeIndex}`}>
                <PaperStyled>
                  <TimeIntervalField
                    timeIndex={timeIndex}
                    title={title}
                    intervalIndex={intervalIndex}
                    intervals={intervals}
                    setIntervals={setIntervals}
                    error={!!errorMessage}
                  />
                </PaperStyled>
              </Grid>
            ))}
          </Grid>
        ))}
      </Grid>
    </Grid>
  );
};

export default DayTimeIntervalField;
