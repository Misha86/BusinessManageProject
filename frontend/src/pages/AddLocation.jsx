import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ManagerService } from '../services/auth.service';
import { Box, Typography } from '@mui/material';
import LocationForm from '../components/LocationForm/LocationForm';

const weekDays = {
  Mon: [],
  Tue: [],
  Wed: [],
  Thu: [],
  Fri: [],
  Sat: [],
  Sun: [],
};

const formFields = [
  { title: 'name', type: 'text', required: true, helpText: 'This field is required' },
  { title: 'address', type: 'text', required: false, helpText: 'This field is required' },
  { title: 'working_time', weekDays: weekDays, required: true, helpText: 'This field is required' },
];

const AddLocation = () => {
  const [location, setLocation] = useState({});
  const [error, setError] = useState({});
  const router = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await ManagerService.addLocation(location);
      router('/');
    } catch (error) {
      console.log(error.response.data);
      setError(error.response.data);
    }
  };
  return (
    <Box mt={3} sx={{ paddingLeft: '25%', width: '50%' }}>
      <Typography component="h5" variant="h5" mb={2} color="primary">
        Add Location
      </Typography>
      <LocationForm
        formFields={formFields}
        location={location}
        setLocation={setLocation}
        handleSubmit={handleSubmit}
        error={error}
      />
    </Box>
  );
};

export default AddLocation;
