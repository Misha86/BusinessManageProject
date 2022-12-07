import React from 'react';
import { Typography } from '@mui/material';
import DayTimeIntervalField from './DayTimeIntervalField';

const WorkingTimeField = ({ field, setLocation, error, location }) => {
  const getTimeValue = (value) => {
    return value.length >= 4 && !value.includes(':') ? `${value.slice(0, 2)}:${value.slice(2)}` : value;
  };

  const handleWorkingTime = (event) => {
    const [weekDay, timeIndex] = event.target.id.split('-');
    let timeInterval = location[field.title][weekDay];
    const fieldValue = event.target.value;

    timeInterval[parseInt(timeIndex)] = getTimeValue(fieldValue);
    timeInterval[0] === undefined && (timeInterval[0] = '');
    timeInterval.every((item) => item === '') && (timeInterval = []);

    setLocation({ ...location, [field.title]: { ...location[field.title], [weekDay]: timeInterval } });
  };

  return (
    <div>
      <Typography component="h6" variant="h6" color={error[field.title] ? 'error' : 'grey'}>
        Working time
      </Typography>
      {field.weekDays.map((weekDay) => (
        <DayTimeIntervalField
          key={weekDay}
          field={field}
          error={error}
          handler={handleWorkingTime}
          workingTime={location[field.title]}
          weekDay={weekDay}
        />
      ))}
    </div>
  );
};

export default WorkingTimeField;
