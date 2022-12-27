import React, { useState, useEffect } from 'react';
import { TextField, FormControl, FormHelperText } from '@mui/material';
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

  useEffect(() => {
    if (!!stringDateTime) {
      handler(stringDateTime, fieldTitle);
    }
  }, [stringDateTime]);

  return (
    <div>
      <ErrorField errorMessage={errorMessage} />

      <FormControl sx={{ width: '100%' }}>
        <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="uk">
          <DateTimePicker
            label={fieldInfo.label}
            renderInput={(params) => (
              <TextField {...params} error={!!errorMessage} variant="standard" required={fieldInfo.required} />
            )}
            value={value || null}
            onChange={(newValue) => {
              setNewValue(newValue);
            }}
            minDate={dayjs()}
            maxDate={dayjs().add(45, 'day')}
            size="small"
            minutesStep={5}
            minTime={dayjs('7:00', 'H:mm')}
            maxTime={dayjs('22:00', 'H:mm')}
            {...props}
          />
        </LocalizationProvider>
      </FormControl>
      <FormHelperText error={!!errorMessage} id={`${fieldTitle}-helper-text`}>
        {fieldInfo.help_text}
      </FormHelperText>
    </div>
  );
};

export default DateTimeField;
