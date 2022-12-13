import React from 'react';
import { Paper, Box } from '@mui/material';
import FormField from './FormField';
import Message from '../Message';
import FormTitle from './FormTitle';
import ErrorDetail from './ErrorDetail';
import SubmitButton from './SubmitButton';
import ChoiceField from './ChoiceField';

const Form = ({ formFields, formTitle, data, setData, handleSubmit, error, showMessage }) => {

  const handleFormFields = (event, fieldTitle, typeField) => {
    const textValue = typeField === 'file' ? event.target.files[0] : event.target.value;
    setData({ ...data, [fieldTitle]: textValue });
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
                handler={handleFormFields}
                value={data[fieldTitle] || ''}
                errorMessage={error[fieldTitle]}
              />
            ) : (
              <FormField
                key={fieldTitle}
                fieldTitle={fieldTitle}
                fieldInfo={fieldInfo}
                errorMessage={error[fieldTitle]}
                handler={handleFormFields}
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
