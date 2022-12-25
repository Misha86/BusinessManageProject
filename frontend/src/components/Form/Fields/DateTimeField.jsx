import React, { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import dayjs from 'dayjs';
import ErrorField from '../ErrorField';
import useStringDateTime from '../../../hooks/useStringDateTime';
import 'dayjs/locale/uk';

const DateTimeField = ({ fieldTitle, fieldInfo, errorMessage, handler, value, props }) => {
  const [newValue, setNewValue] = useState(null);
  const stringDateTime = useStringDateTime(newValue);

//   console.log(newValue);
//   console.log(value, 'value');

  useEffect(() => {
    if (!!stringDateTime) {
      handler(stringDateTime, fieldTitle);
    }
  }, [stringDateTime]);

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="uk">
      <ErrorField errorMessage={errorMessage} />

      <DateTimePicker
        label={fieldInfo.label}
        renderInput={(params) => <TextField {...params} variant="standard" />}
        value={value || ''}
        onChange={(newValue) => {
          setNewValue(newValue);
        }}
        minDate={dayjs()}
        maxDate={dayjs().add(45, 'day')}
        required={fieldInfo.required}   
        size="small"
        minutesStep={5}
        minTime={dayjs('7:00', 'H:mm')}
        maxTime={dayjs('22:00', 'H:mm')}
        {...props}
      />
    </LocalizationProvider>
  );
};

export default DateTimeField;
