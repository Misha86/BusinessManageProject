import React from 'react';
import { FormControl, TextField, FormHelperText } from '@mui/material';

const TimeIntervalField = ({ error, intervalIndex, intervals, setIntervals, timeIndex, title }) => {
  const getTimeValue = (value) => {
    return value.length >= 4 && !value.includes(':') ? `${value.slice(0, 2)}:${value.slice(2)}` : value;
  };

  const timeIntervalHandler = (event) => {
    const fieldValue = event.target.value;
    let timeInterval = intervals[intervalIndex];
    timeInterval[timeIndex] = getTimeValue(fieldValue);
    timeInterval[0] === undefined && (timeInterval[0] = '');
    timeInterval.every((item) => item !== '') && (intervals[intervalIndex] = timeInterval);
    intervals[intervalIndex] = timeInterval;
    setIntervals([...intervals]);
  };

  return (
    <FormControl>
      <TextField
        id={`${title}${intervalIndex}${timeIndex}`}
        label={title}
        value={intervals[intervalIndex]?.[timeIndex] || ''}
        variant="standard"
        size="small"
        onChange={timeIntervalHandler}
        error={error}
        inputProps={{ maxLength: 5 }}
      />
      <FormHelperText id={`${intervalIndex}-${timeIndex}-helper-text`} error={error}>
        Format HH:MM
      </FormHelperText>
    </FormControl>
  );
};

export default TimeIntervalField;
