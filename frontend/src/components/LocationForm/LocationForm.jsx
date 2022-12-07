import React, { useState } from 'react';
import { Paper, Button, Typography } from '@mui/material';
import FormField from '../Form/FormField';
import WorkingTime from './WorkingTimeField';
import { ManagerService } from '../../services/auth.service';
import { getEmptySchedule } from '../../utils';

const LocationForm = ({ formFields, weekDays }) => {
  const [location, setLocation] = useState({ working_time: getEmptySchedule(weekDays) });
  const [error, setError] = useState({});

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await ManagerService.addLocation(location);
      setLocation({ working_time: getEmptySchedule(weekDays) });
      setError({});
    } catch (error) {
      console.log(error);
      setError(error.response.data);
    }
  };

  const handleTextInput = (event) => {
    const textValue = event.target.value;
    setLocation({ ...location, [event.target.id]: textValue });
  };

  return (
    <form onSubmit={handleSubmit}>
      <Paper elevation={3} sx={{ padding: '6%' }}>
        {error && error.detail && (
          <Typography component="p" variant="p" mb={2} color="error">
            {error.detail}
          </Typography>
        )}

        {formFields.map((field) =>
          field.title === 'working_time' ? (
            <WorkingTime key={field.title} field={field} error={error} location={location} setLocation={setLocation} />
          ) : (
            <FormField key={field.title} field={field} error={error} data={location} handler={handleTextInput} />
          )
        )}

        <Button variant="contained" color="primary" type="submit">
          Submit
        </Button>
      </Paper>
    </form>
  );
};

export default LocationForm;
