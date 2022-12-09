import React from 'react';
import { Typography } from '@mui/material';
import DayTimeIntervalField from './DayTimeIntervalField';

const WorkingTimeField = ({ field, data, error, setData }) => {
  const getTimeValue = (value) => {
    return value.length >= 4 && !value.includes(':') ? `${value.slice(0, 2)}:${value.slice(2)}` : value;
  };

  const handleWorkingTime = (event) => {
    const [weekDay, timeIndex] = event.target.id.split('-');
    let timeInterval = data[field.title][weekDay];
    const fieldValue = event.target.value;

    timeInterval[parseInt(timeIndex)] = getTimeValue(fieldValue);
    timeInterval[0] === undefined && (timeInterval[0] = '');
    timeInterval.every((item) => item === '') && (timeInterval = []);

    setData({ ...data, [field.title]: { ...data[field.title], [weekDay]: timeInterval } });
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
          workingTime={data[field.title]}
          weekDay={weekDay}
        />
      ))}
    </div>
  );
};

export default WorkingTimeField;
