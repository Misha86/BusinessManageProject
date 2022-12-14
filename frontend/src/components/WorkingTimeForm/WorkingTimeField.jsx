import React, { useCallback } from 'react';
import { Typography } from '@mui/material';
import DayTimeIntervalField from './DayTimeIntervalField';

const WorkingTimeField = ({ fieldTitle, fieldInfo, data, error, setData }) => {
  const handleWorkingTime = useCallback(
    (dayTimeIntervals) => {
      setData({ ...data, [fieldTitle]: { ...data[fieldTitle], ...dayTimeIntervals } });
    },
    [data, setData, fieldTitle]
  );

  return (
    <div>
      <Typography component="h6" variant="h6" mb={1} color={error[fieldTitle] ? 'error' : 'grey'}>
        Working time
      </Typography>
      {Object.entries(fieldInfo.children).map(([weekDay, _]) => (
        <DayTimeIntervalField
          key={weekDay}
          fieldTitle={fieldTitle}
          error={error}
          handler={handleWorkingTime}
          weekDay={weekDay}
        />
      ))}
    </div>
  );
};

export default WorkingTimeField;
