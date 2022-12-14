import React, { useEffect, useState, useContext } from 'react';
import { InputLabel, Typography, Grid } from '@mui/material';
import TimeIntervalField from './TimeIntervalField';
import { PaperStyled } from '../../styles/Paper.styled';
import { WorkingFormContext } from '../../../context/index';
import AddIntervalButton from '../UI/AddIntervalButton';
import RemoveIntervalButton from '../UI/RemoveIntervalButton';
import ErrorField from '../../Form/ErrorField';

const WorkingTimeField = ({ weekDay, fieldTitle, error, handler, data }) => {
  const errorMessage = error?.[fieldTitle]?.[weekDay];
  const dayIntervals = data[fieldTitle]?.[weekDay];

  const [intervals, setIntervals] = useState(
    !!dayIntervals.length && typeof dayIntervals[0] === 'string' ? [dayIntervals] : dayIntervals
  );
  const { countOfTimeIntervals } = useContext(WorkingFormContext);

  useEffect(() => {
    const timeIntervals = intervals.filter((interval) => interval.length > 0);
    const dayTimeIntervals = {
      [weekDay]: countOfTimeIntervals === 1 && timeIntervals.length === 1 ? timeIntervals[0] : timeIntervals,
    };
    handler(fieldTitle, dayTimeIntervals);
  }, [intervals]);

  const wrapButton = ({ children }) => (
    <Grid item xs={12} md={12}>
      {children}
    </Grid>
  );

  return (
    <Grid container spacing={1}>
      {!!errorMessage && (
        <Grid item xs={12} md={12} >
          <ErrorField errorMessage={errorMessage} />
        </Grid>
      )}

      <Grid justifyContent="flex-end" item xs={4} md={2}>
        <Grid item xs={12} md={12}>
          <InputLabel error={!!errorMessage}>{weekDay}</InputLabel>
        </Grid>

        <AddIntervalButton
          intervals={intervals}
          setIntervals={setIntervals}
          count={countOfTimeIntervals}
          component={wrapButton}
        />

        <RemoveIntervalButton intervals={intervals} setIntervals={setIntervals} component={wrapButton} />
      </Grid>

      <Grid container item xs={8} md={10}>
        {intervals.length === 0 && (
          <Grid item mt={3}>
            <Typography component="p" variant="p">
              {`Add working interval for ${weekDay}`}
            </Typography>
          </Grid>
        )}

        <Grid container item spacing={1} mb={1}>
          {intervals.map((_, intervalIndex) => (
            <Grid item xs={12} md={12} key={intervalIndex}>
              <PaperStyled>
                <TimeIntervalField
                  intervalIndex={intervalIndex}
                  intervals={intervals}
                  setIntervals={setIntervals}
                  error={!!errorMessage}
                />
              </PaperStyled>
            </Grid>
          ))}
        </Grid>
      </Grid>
    </Grid>
  );
};

export default WorkingTimeField;
