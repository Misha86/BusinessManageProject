import React from 'react';
import { Box, Typography } from '@mui/material';
import LocationForm from '../components/LocationForm/LocationForm';
import {weekDays} from '../utils'


const formFields = [
  { title: 'specialist', type: 'text', required: true, helpText: 'This field is required' },
  { title: 'working_time', weekDays: weekDays },
];

const AddSchedule = () => {
  return (
    <Box mt={3} sx={{ paddingLeft: '30%', width: '40%' }}>
      <Typography component="h5" variant="h5" color="primary">
        Add Schedule
      </Typography>
      <LocationForm formFields={formFields} weekDays={weekDays} />
    </Box>
  );
};

export default AddSchedule;
