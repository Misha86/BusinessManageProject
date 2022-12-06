import React from 'react';
import { Typography, Button, Paper, Box } from '@mui/material';
import FormField from './FormField';

const Form = ({ formFields, formTitle, data, setData, handleSubmit, error }) => {
  const handleTextInput = (event) => {
    const textValue = event.target.value;
    setData({ ...data, [event.target.id]: textValue });
  };

  const handleFileInput = (event) => {
    const fileValue = event.target.files[0];
    setData({ ...data, [event.target.id]: fileValue });
  };

  const chooseInputHandler = (event) => {
    event.target.type === 'file' ? handleFileInput(event) : handleTextInput(event);
  };

  return (
    <Box mt={3} sx={{ paddingLeft: '30%', width: '40%' }}>
      <Typography component="h5" variant="h5" mb={2} color="primary">
        {formTitle}
      </Typography>
      <form onSubmit={handleSubmit}>
        <Paper elevation={3} sx={{ padding: '6%' }}>
          {error && error.detail && (
            <Typography component="p" variant="p" mb={2} color="error">
              {error.detail}
            </Typography>
          )}

          {formFields.map((field) => (
            <FormField key={field.title} field={field} error={error} handler={chooseInputHandler} />
          ))}
          <Button variant="contained" color="primary" type="submit">
            Submit
          </Button>
        </Paper>
      </form>
    </Box>
  );
};

export default Form;
