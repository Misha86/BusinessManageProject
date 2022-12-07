import React from 'react';
import { FormControl, TextField, FormHelperText } from '@mui/material';

const TimeIntervalField = ({ weekDay, item, handler, workingTime, error }) => {
  return (
    <FormControl sx={{ width: '35%', ml: '5%' }}>
      <TextField
        id={`${weekDay}-${item.index}`}
        label={item.title}
        value={workingTime[weekDay][item.index] || ''}
        variant="standard"
        size="small"
        onChange={handler}
        error={error}
        inputProps={{ maxLength: 5 }}
      />
      <FormHelperText id={`${weekDay}-${item.repString}-helper-text`} error={error}>
        Format HH:MM
      </FormHelperText>
    </FormControl>
  );
};

export default TimeIntervalField;
