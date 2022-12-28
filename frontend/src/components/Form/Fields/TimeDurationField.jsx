import React, { useState, useEffect, useMemo } from 'react';
import { TextField, FormControl, FormHelperText } from '@mui/material';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import dayjs from 'dayjs';
import ErrorField from '../ErrorField';
import useStringTime from '../../../hooks/useStringTime';

const TimeDurationField = ({ fieldTitle, fieldInfo, errorMessage, handler, value, props }) => {
  const [newValue, setNewValue] = useState(null);
  const stringTime = useStringTime(newValue, true);

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
    <div>
      <ErrorField errorMessage={errorMessage} />

      <FormControl sx={{ width: '100%' }}>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <TimePicker
            label={fieldInfo.label}
            ampm={false}
            openTo="minutes"
            renderInput={(params) => (
              <TextField {...params} error={!!errorMessage} variant="standard" required={fieldInfo.required} />
            )}
            value={fieldValue}
            onChange={(newValue) => {
              setNewValue(newValue);
            }}
            size="small"
            minutesStep={5}
            minTime={dayjs('0:15', 'H:mm')}
            maxTime={dayjs('1:30', 'H:mm')}
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

export default TimeDurationField;
