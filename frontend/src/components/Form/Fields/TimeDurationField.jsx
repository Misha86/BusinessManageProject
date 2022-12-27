import React, { useState, useEffect, useMemo } from 'react';
import TextField from '@mui/material/TextField';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import dayjs from 'dayjs';
import ErrorField from '../ErrorField';
import useStringTime from '../../../hooks/useStringTime';

const TimeDurationField = ({ fieldTitle, fieldInfo, errorMessage, handler, value, props }) => {
  const [newValue, setNewValue] = useState(null);
  const stringTime = useStringTime(newValue);

  const fieldValue = useMemo(() => {
    const timeValue = dayjs(value, 'H:mm');
    return timeValue.isValid() ? timeValue : null;
  }, [value]);

  useEffect(() => {
    if (!!stringTime) {
      handler(stringTime, fieldTitle);
    }
  }, [stringTime]);

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <ErrorField errorMessage={errorMessage} />

      <TimePicker
        label={fieldInfo.label}
        ampm={false}
        openTo="minutes"
        renderInput={(params) => <TextField {...params} variant="standard" required={fieldInfo.required} />}
        value={fieldValue}
        onChange={(newValue) => {
          setNewValue(newValue);
        }}
        size="small"
        minutesStep={5}
        minTime={dayjs('0:05', 'H:mm')}
        maxTime={dayjs('1:30', 'H:mm')}
        {...props}
      />
    </LocalizationProvider>
  );
};

export default TimeDurationField;
