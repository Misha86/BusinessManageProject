import React, { useEffect, useState, useMemo } from 'react';
import { FormControl, FormHelperText } from '@mui/material';
import { TimeRangeInput } from '@mantine/dates';
import dayjs from 'dayjs';
import useStringTime from '../../../hooks/useStringTime';

const TimeIntervalField = ({ error, intervalIndex, intervals, setIntervals }) => {
  const [value, setValue] = useState([null, null]);
  const startTime = useStringTime(value[0] && dayjs(value[0]));
  const endTime = useStringTime(value[1] && dayjs(value[1]));

  const fieldValue = useMemo(() => {
    const defaultValue = intervals[intervalIndex].map((item) => (item ? dayjs(item, 'H:mm').toDate() : null));
    return defaultValue;
  }, [intervals[intervalIndex]]);


  useEffect(() => {
    if (value.every((item) => item !== null)) {
      intervals[intervalIndex] = [startTime, endTime];
      setIntervals([...intervals]);
    }
  }, [value]);

  return (
    <FormControl sx={{ width: '100%' }}>
      <TimeRangeInput label="Working interval" value={fieldValue} onChange={setValue} clearable error={error} />

      <FormHelperText id={`${intervalIndex}-helper-text`} error={error}>
        Format HH:MM
      </FormHelperText>
    </FormControl>
  );
};

export default TimeIntervalField;
