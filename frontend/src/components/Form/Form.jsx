import React from 'react';
import { Paper, Box } from '@mui/material';
import FormField from './FormField';
import Message from '../Message';
import FormTitle from './FormTitle';
import ErrorDetail from './ErrorDetail';
import SubmitButton from './SubmitButton';

const Form = ({ formFields, formTitle, data, setData, handleSubmit, error, showMessage }) => {
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
      <FormTitle formTitle={formTitle} />
      <form onSubmit={handleSubmit}>
        <Message showMessage={showMessage} messageText="The Specialist was added!" />

        <Paper elevation={3} sx={{ padding: '6%' }}>
          <ErrorDetail error={error} />

          {formFields.map((field) => (
            <FormField key={field.title} field={field} error={error} handler={chooseInputHandler} data={data} />
          ))}
          <SubmitButton/>
        </Paper>
      </form>
    </Box>
  );
};

export default Form;
