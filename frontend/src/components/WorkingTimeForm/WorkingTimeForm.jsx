import React, { useState } from 'react';
import { Paper, Box } from '@mui/material';
import FormField from '../Form/FormField';
import WorkingTimeField from './WorkingTimeField';
import { getEmptySchedule, messageTimeout } from '../../utils';
import Message from '../Message';
import FormTitle from '../Form/FormTitle';
import ErrorDetail from '../Form/ErrorDetail';
import { weekDays } from '../../utils';
import SubmitButton from '../Form/SubmitButton';

const WorkingTimeForm = ({ formTitle, formFields, service, messageText }) => {
  const [data, setData] = useState({ working_time: getEmptySchedule(weekDays) });
  const [error, setError] = useState({});
  const [showMessage, setShowMessage] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await service(data);
      setData({});
      setError({});
      setShowMessage(true);
      messageTimeout(7000, setShowMessage);
      localStorage.setItem('created', 'true');
    } catch (error) {
      console.log(error);
      setError(error.response.data);
    }
  };

  const handleTextInput = (event) => {
    const textValue = event.target.value;
    setData({ ...data, [event.target.id]: textValue });
  };

  return (
    <Box mt={3} sx={{ paddingLeft: '30%', width: '40%' }}>
      <FormTitle formTitle={formTitle} />
      <form onSubmit={handleSubmit}>
        <Message showMessage={showMessage} messageText={messageText} />

        <Paper elevation={3} sx={{ padding: '6%' }}>
          <ErrorDetail error={error} />

          {formFields.map((field) =>
            field.title === 'working_time' ? (
              <WorkingTimeField key={field.title} field={field} error={error} data={data} setData={setData} />
            ) : (
              <FormField key={field.title} field={field} error={error} data={data} handler={handleTextInput} />
            )
          )}

          <SubmitButton />
        </Paper>
      </form>
    </Box>
  );
};

export default WorkingTimeForm;
