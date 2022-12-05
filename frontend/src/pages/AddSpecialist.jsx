import { Typography, Box } from '@mui/material';
import React from 'react';
import AddSpecialistForm from '../components/SpecialistForm/SpecialistForm';


const formFields = [
  { title: 'email', type: 'email', required: true, helpText: 'This field is required' },
  { title: 'first_name', type: 'text', required: true, helpText: 'This field is required' },
  { title: 'last_name', type: 'text', required: true, helpText: 'This field is required' },
  { title: 'patronymic', type: 'text', required: true, helpText: 'This field is not required' },
  { title: 'position', type: 'text', required: true, helpText: 'This field is required' },
  { title: 'bio', type: 'textarea', required: false, helpText: 'This field is not required' },
  { title: 'avatar', type: 'file', required: false, helpText: 'Get Avatar to the profile' },
];

const AddSpecialist = () => {
  return (
    <Box mt={3} sx={{ paddingLeft: '30%', width: '40%' }}>
      <Typography component="h5" variant="h5" mb={2} color="primary">
        Add Specialist
      </Typography>
      <AddSpecialistForm formFields={formFields} />
    </Box>
  );
};

export default AddSpecialist;
