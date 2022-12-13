import React from 'react';
import { Paper, Box } from '@mui/material';
import FormField from './FormField';
import Message from '../Message';
import FormTitle from './FormTitle';
import ErrorDetail from './ErrorDetail';
import SubmitButton from './SubmitButton';
import ChoiceField from './ChoiceField';

const Form = ({ formFields, formTitle, data, setData, handleSubmit, error, showMessage }) => {
  const handleTextInput = (event) => {
    const textValue = event.target.value;
    setData({ ...data, [event.target.id]: textValue });
  };

  const handleFileInput = (event) => {
    const fileValue = event.target.files[0];
    setData({ ...data, [event.target.id]: fileValue });
  };

  const handleChoiceInput = (event, fieldTitle) => {
    const textValue = event.target.value;
    setData({ ...data, [fieldTitle]: textValue });
    console.log(event);
  };

  return (
    <Box mt={3} sx={{ paddingLeft: '30%', width: '40%' }}>
      <FormTitle formTitle={formTitle} />
      <form onSubmit={handleSubmit}>
        <Message showMessage={showMessage} messageText="The Specialist was added!" />

        <Paper elevation={3} sx={{ padding: '6%' }}>
          <ErrorDetail error={error} />

          {Object.entries(formFields).map(([fieldTitle, fieldInfo]) =>
            fieldInfo.type === 'choice' ? (
              <ChoiceField
                key={fieldTitle}
                fieldTitle={fieldTitle}
                fieldInfo={fieldInfo}
                handler={handleChoiceInput}
                value={data[fieldTitle] || ''}
                errorMessage={error[fieldTitle]}
              />
            ) : (
              <FormField
                key={fieldTitle}
                fieldTitle={fieldTitle}
                fieldInfo={fieldInfo}
                errorMessage={error[fieldTitle]}
                handler={fieldInfo.type === 'file' ? handleFileInput : handleTextInput}
                type={fieldInfo.type}
                value={fieldInfo.type !== 'file' ? data[fieldTitle] || '' : undefined}
                multiline={fieldInfo.type === 'textarea' && true}
              />
            )
          )}

          <SubmitButton />
        </Paper>
      </form>
    </Box>
  );
};

export default Form;
