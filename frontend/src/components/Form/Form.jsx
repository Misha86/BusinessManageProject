import React, { useState } from 'react';
import { Paper, Box, Typography } from '@mui/material';
import FormField from './Fields/FormField';
import Message from '../Message';
import FormTitle from './FormTitle';
import ErrorDetail from './ErrorDetail';
import SubmitButton from './SubmitButton';
import ChoiceField from './Fields/ChoiceField';
import WorkingTimeField from './Fields/WorkingTimeField';
import dayjs from 'dayjs';
import DateTimeField from './Fields/DateTimeField';

const Form = ({ formFields, formTitle, data, setData, handleSubmit, error, showMessage, messageText }) => {

  const handleTextField = (event, fieldTitle, typeField) => {
    const textValue = typeField === 'file' ? event.target.files[0] : event.target.value;
    setData({ ...data, [fieldTitle]: textValue });
  };

  const handleDateTimeField = (newValue, fieldTitle) => {
    setData({ ...data, [fieldTitle]: newValue });
  };

  const handleWorkingTime = (fieldTitle, dayTimeIntervals) => {
    setData({ ...data, [fieldTitle]: { ...data[fieldTitle], ...dayTimeIntervals } });
  };

  return (
    <Box mt={3} sx={{ paddingLeft: '30%', width: '40%' }}>
      <FormTitle formTitle={formTitle} />
      <form onSubmit={handleSubmit}>
        <Message showMessage={showMessage} messageText={messageText} />

        <Paper elevation={3} sx={{ padding: '6%' }}>
          <ErrorDetail error={error} />

          {Object.entries(formFields).map(([fieldTitle, fieldInfo]) => {
            if (fieldInfo.type === 'choice') {
              return (
                <ChoiceField
                  key={fieldTitle}
                  fieldTitle={fieldTitle}
                  fieldInfo={fieldInfo}
                  handler={handleTextField}
                  value={data[fieldTitle] || ''}
                  errorMessage={error?.[fieldTitle]}
                />
              );
            } else if (fieldTitle === 'working_time') {
              return (
                <div key={fieldTitle}>
                  <Typography component="h6" variant="h6" mb={1} color={error?.[fieldTitle] ? 'error' : 'grey'}>
                    {fieldInfo.label}
                  </Typography>
                  {Object.entries(fieldInfo.children).map(([weekDay, _]) => (
                    <WorkingTimeField
                      key={weekDay}
                      data={data}
                      setData={setData}
                      fieldTitle={fieldTitle}
                      error={error}
                      handler={handleWorkingTime}
                      weekDay={weekDay}
                    />
                  ))}
                </div>
              );
            } else if (fieldInfo.type === 'datetime') {
              return (
                <DateTimeField
                  key={fieldTitle}
                  fieldTitle={fieldTitle}
                  fieldInfo={fieldInfo}
                  value={data[fieldTitle]}
                  handler={handleDateTimeField}
                  errorMessage={error?.[fieldTitle]}
                />
              );
            } else {
              return (
                <FormField
                  key={fieldTitle}
                  fieldTitle={fieldTitle}
                  fieldInfo={fieldInfo}
                  errorMessage={error?.[fieldTitle]}
                  handler={handleTextField}
                  type={fieldInfo.type}
                  value={fieldInfo.type !== 'file' ? data[fieldTitle] || '' : undefined}
                  multiline={fieldInfo.type === 'textarea' && true}
                  props={fieldInfo.props}
                />
              );
            }
          })}

          <SubmitButton />
        </Paper>
      </form>
    </Box>
  );
};

export default Form;
