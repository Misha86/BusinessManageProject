import React from 'react';
import { Box, InputLabel, Typography } from '@mui/material';
import TimeIntervalField from './TimeIntervalField';

const DayTimeIntervalField = ({ weekDay, field, error, handler, workingTime }) => {
  const isError = (field) => !!error[field.title]?.[weekDay];

  const timeInterval = [
    { title: 'Start time', index: 0 },
    { title: 'End time', index: 1 },
  ];
  return (
    <Box>
      {isError(field) && (
        <Typography component="p" variant="p" mb={2} color="error">
          {error[field.title]?.[weekDay]}
        </Typography>
      )}

      <InputLabel sx={{ display: 'inline-block', width: '20%' }} error={isError(field)}>
        {weekDay}
      </InputLabel>
      {timeInterval.map((item) => (
        <TimeIntervalField
          key={item.title}
          weekDay={weekDay}
          item={item}
          handler={handler}
          workingTime={workingTime}
          error={isError(field)}
        />
      ))}
    </Box>
  );
};

export default DayTimeIntervalField;
