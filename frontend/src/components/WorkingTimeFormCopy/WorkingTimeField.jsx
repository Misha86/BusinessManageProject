import React from 'react';
import { Typography } from '@mui/material';
import DayTimeIntervalField from './DayTimeIntervalField';

const WorkingTimeField = ({ field, data, error, setData }) => {

  const handleWorkingTime = (dayTimeIntervals) => {
    setData({ ...data, [field.title]: { ...data[field.title], ...dayTimeIntervals } });
  };

  return (
    <div>
      <Typography component="h6" variant="h6" mb={1} color={error[field.title] ? 'error' : 'grey'}>
        Working time
      </Typography>
      {field.weekDays.map((weekDay) => (
        <DayTimeIntervalField
          key={weekDay}
          field={field}
          error={error}
          handler={handleWorkingTime}
          weekDay={weekDay}
        />
      ))}
    </div>
  );
};

export default WorkingTimeField;
