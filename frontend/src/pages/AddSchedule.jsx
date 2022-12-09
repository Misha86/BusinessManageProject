import React from 'react';
import { Box, Typography } from '@mui/material';
import WorkingTimeForm from '../components/WorkingTimeFormCopy/WorkingTimeForm';
import { weekDays } from '../utils';
import { ManagerService } from '../services/auth.service';

const formFields = [
  { title: 'specialist', type: 'email', required: true, helpText: 'This field is required. Input specialist email.' },
  { title: 'working_time', weekDays: weekDays },
];

const AddSchedule = () => {
  const messageText = 'The schedule was added!';
  return (
    <Box mt={3} sx={{ paddingLeft: '30%', width: '40%' }}>
      <Typography component="h5" variant="h5" color="primary">
        Add Schedule
      </Typography>
      <WorkingTimeForm
        formFields={formFields}
        weekDays={weekDays}
        service={ManagerService.addSchedule}
        messageText={messageText}
      />
    </Box>
  );
};

export default AddSchedule;
