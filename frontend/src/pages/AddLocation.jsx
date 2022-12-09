import React from 'react';
import { Box, Typography } from '@mui/material';
import WorkingTimeForm from '../components/WorkingTimeForm/WorkingTimeForm';
import { weekDays } from '../utils';
import { ManagerService } from '../services/auth.service';

const formFields = [
  { title: 'name', type: 'text', required: true, helpText: 'This field is required' },
  { title: 'address', type: 'textarea', required: false, helpText: 'This field is not required' },
  { title: 'working_time', weekDays: weekDays },
];

const AddLocation = () => {
  const messageText = 'The location was added!';
  return (
    <Box mt={3} sx={{ paddingLeft: '30%', width: '40%' }}>
      <Typography component="h5" variant="h5" color="primary">
        Add Location
      </Typography>
      <WorkingTimeForm
        formFields={formFields}
        weekDays={weekDays}
        service={ManagerService.addLocation}
        messageText={messageText}
      />
    </Box>
  );
};

export default AddLocation;
