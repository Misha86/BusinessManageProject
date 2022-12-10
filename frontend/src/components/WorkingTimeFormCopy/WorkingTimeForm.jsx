import React, { useState } from 'react';
import { Paper, Button, Typography } from '@mui/material';
import FormField from '../Form/FormField';
import WorkingTime from './WorkingTimeField';
import { getEmptySchedule, messageTimeout } from '../../utils';
import Message from '../Message';


const WorkingTimeForm = ({ formFields, weekDays, service, messageText }) => {
  const [data, setData] = useState({ working_time: getEmptySchedule(weekDays) });
  const [error, setError] = useState({});
  const [showMessage, setShowMessage] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await service(data);
      setData({ working_time: getEmptySchedule(weekDays) });
      setError({});
      setShowMessage(true);
      messageTimeout(7000, setShowMessage);
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
    <form onSubmit={handleSubmit}>
      <Message showMessage={showMessage} messageText={messageText} />

      <Paper elevation={3} sx={{ padding: '6%' }}>
        {error && error.detail && (
          <Typography component="p" variant="p" mb={2} color="error">
            {error.detail}
          </Typography>
        )}

        {formFields.map((field) =>
          field.title === 'working_time' ? (
            <WorkingTime key={field.title} field={field} error={error} data={data} setData={setData} />
          ) : (
            <FormField key={field.title} field={field} error={error} data={data} handler={handleTextInput} />
          )
        )}

        <Button variant="contained" color="primary" type="submit" pt={1}>
          Submit
        </Button>
      </Paper>
    </form>
  );
};

export default WorkingTimeForm;
