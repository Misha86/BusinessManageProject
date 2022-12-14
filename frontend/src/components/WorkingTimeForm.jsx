import React, { useState } from 'react';
import { getEmptySchedule, messageTimeout } from '../utils';
import { weekDays } from '../utils';
import Form from './Form/Form';

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
      console.log(error.response);
      setError(error.response?.data);
    }
  };

  return (
    <>
      <Form
        formFields={formFields}
        formTitle={formTitle}
        data={data}
        setData={setData}
        handleSubmit={handleSubmit}
        error={error}
        showMessage={showMessage}
      />
    </>
  );
};

export default WorkingTimeForm;
