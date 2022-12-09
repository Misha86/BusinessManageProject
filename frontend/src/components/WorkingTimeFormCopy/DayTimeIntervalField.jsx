import React, { useState } from 'react';
import { InputLabel, Typography, Grid, Paper, Icon, IconButton } from '@mui/material';
import TimeIntervalField from './TimeIntervalField';
import { styled } from '@mui/material/styles';

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

const DayTimeIntervalField = ({ weekDay, field, error, handler, workingTime }) => {
  const isError = (field) => !!error[field.title]?.[weekDay];
  const [intervals, setIntervals] = useState([[]]);

  const timeInterval = [
    { title: 'Start time', index: 0 },
    { title: 'End time', index: 1 },
  ];

  const removeInterval = () => {
    if (intervals.length > 1) {
      intervals.pop();
      setIntervals([...intervals]);
    }
  };

  const addInterval = () => {
    if (intervals.length < 4) {
      setIntervals([...intervals, []]);
    }
  };

  console.log(intervals);

  return (
    <Grid container spacing={1}>
      {isError(field) && (
        <Grid item xs={12} md={12}>
          <Typography component="p" variant="p" color="error">
            {error[field.title]?.[weekDay]}
          </Typography>
        </Grid>
      )}
      <Grid item xs={4} md={2}>
        <InputLabel error={isError(field)}>{weekDay}</InputLabel>

        {intervals.length < 4 && (
        <IconButton aria-label="add time interval" onClick={() => addInterval()}>
          <Icon color="primary">add_circle</Icon>
        </IconButton>
        )}

        {intervals.length > 1 && (
          <IconButton aria-label="remove time interval" onClick={() => removeInterval()}>
            <Icon color="primary">do_not_disturb_on</Icon>
          </IconButton>
        )}

      </Grid>
      <Grid container item xs={8} md={10}>
        {intervals.map((interval, index) => (
          <Grid container item spacing={1} mb={1} key={index}>
            {timeInterval.map((item) => (
              <Grid item xs={12} md={6} key={`${index}-${item.index}`}>
                <Item>
                  <TimeIntervalField
                    key={item.title}
                    weekDay={weekDay}
                    item={item}
                    handler={handler}
                    workingTime={workingTime}
                    error={isError(field)}
                  />
                </Item>
              </Grid>
            ))}
          </Grid>
        ))}
      </Grid>
    </Grid>
  );
};

export default DayTimeIntervalField;
