import React, { useState } from 'react';
import { Typography } from '@mui/material';
import DayTimeIntervalField from './DayTimeIntervalField';

const WorkingTimeField = ({ field, setLocation, error, location }) => {
  const [workingTime, setWorkingTime] = useState(field.weekDays);

  const handleWorkingTime = (event) => {
    const [weekDay, index] = event.target.id.split('-');
    workingTime[weekDay][parseInt(index)] = event.target.value;
    const interval = workingTime[weekDay];
    interval.every(item => item === '') && (workingTime[weekDay] = []);
    console.log(workingTime[weekDay]);
    setWorkingTime({ ...workingTime });
    setLocation({ ...location, [field.title]: workingTime });
  };

  return (
    <div>
      <Typography component="h6" variant="h6" color="grey">
        Working time
      </Typography>
      {Object.keys(field.weekDays).map((weekDay) => (
        <DayTimeIntervalField
          key={weekDay}
          field={field}
          error={error}
          handler={handleWorkingTime}
          workingTime={workingTime}
          weekDay={weekDay}
        />
      ))}
    </div>
  );
};

export default WorkingTimeField;
