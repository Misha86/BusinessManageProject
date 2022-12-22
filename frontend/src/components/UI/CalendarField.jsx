import React from 'react';
import { TextField } from '@mui/material';
import dayjs from 'dayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import Stack from '@mui/material/Stack';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';

const CalendarField = ({ setDateData, dateData }) => {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Stack spacing={3}>
        <DatePicker
          views={['day']}
          label="Working date"
          minDate={dayjs()}
          maxDate={dayjs().add(45, 'day')}
          value={dateData}
          onChange={(newValue) => {
            setDateData(newValue);
          }}
          renderInput={(params) => (
            <TextField {...params} helperText={params?.inputProps?.placeholder} variant="standard" />
          )}
        />
      </Stack>
    </LocalizationProvider>
  );
};

export default CalendarField;
