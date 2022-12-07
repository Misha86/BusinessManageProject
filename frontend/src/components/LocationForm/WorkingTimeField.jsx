import React, { useEffect, useState } from 'react';
import { Typography } from '@mui/material';
import DayTimeIntervalField from './DayTimeIntervalField';

const WorkingTimeField = ({ field, setLocation, error, location, isCreated }) => {
  const emptySchedule = field.weekDays.reduce((accumulator, value) => {
    return { ...accumulator, [value]: [] };
  }, {});

  const [workingTime, setWorkingTime] = useState(emptySchedule);

  const getTimeValue = (value) => {
    return value.length >= 4 && !value.includes(':') ? `${value.slice(0, 2)}:${value.slice(2)}` : value;
  };

  const handleWorkingTime = (event) => {
    const [weekDay, timeIndex] = event.target.id.split('-');
    let timeInterval = workingTime[weekDay];
    const fieldValue = event.target.value;
    timeInterval[parseInt(timeIndex)] = getTimeValue(fieldValue);
    timeInterval[0] === undefined && (timeInterval[0] = '');
    timeInterval.every((item) => item === '') && (timeInterval = []);
    // console.log(workingTime);
    setWorkingTime({ ...workingTime });
    setLocation({ ...location, [field.title]: workingTime });  
  };
  
  useEffect(() => {
    setLocation({[field.title]: emptySchedule });
    console.log(location, "-----");
    console.log(emptySchedule, "-33----");

  }, [isCreated]);

  return (
    <div> 
      <Typography component="h6" variant="h6" color="grey">
        Working time
      </Typography>
      {field.weekDays.map((weekDay) => (
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
