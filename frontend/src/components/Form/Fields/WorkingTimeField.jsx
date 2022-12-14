import React, { useEffect, useState, useContext } from 'react';
import { InputLabel, Typography, Grid } from '@mui/material';
import TimeIntervalField from './TimeIntervalField';
import { PaperStyled } from '../../styles/Paper.styled';
import { WorkingFormContext} from '../../../context/index';
import AddIntervalButton from '../UI/AddIntervalButton';
import RemoveIntervalButton from '../UI/RemoveIntervalButton';
import ErrorField from '../../Form/ErrorField';

const WorkingTimeField = ({ weekDay, fieldTitle, error, handler }) => {
  const errorMessage = error[fieldTitle]?.[weekDay];
  const [intervals, setIntervals] = useState([]);
  const { countOfTimeIntervals } = useContext(WorkingFormContext);

  const status = localStorage.getItem('created', 'true');

  useEffect(() => {
    const timeIntervals = intervals.filter((interval) => interval.length > 0);
    const dayTimeIntervals = { [weekDay]: countOfTimeIntervals > 1 ? timeIntervals : timeIntervals[0] };
    handler(fieldTitle, dayTimeIntervals);
    status === 'true' && setIntervals([]);
    localStorage.removeItem('created');
  }, [intervals, status]);

  const wrapButton = ({ children }) => (
    <Grid item xs={12} md={12}>
      {children}
    </Grid>
  );

  return (
    <Grid container spacing={1}>
      <Grid item xs={12} md={12}>
        <ErrorField errorMessage={errorMessage} />
      </Grid>

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

export default WorkingTimeField;
