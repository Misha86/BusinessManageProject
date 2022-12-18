import React, { useState } from 'react';
import { getEmptySchedule, messageTimeout } from '../utils';
import { weekDays } from '../utils';
import Form from './Form/Form';
import useFetching from '../hooks/useFetching';
import Loading from './Loading';

const WorkingTimeForm = ({ formTitle, service, messageText, formFields }) => {
  const [data, setData] = useState({ working_time: getEmptySchedule(weekDays) });
  const [showMessage, setShowMessage] = useState(false);
  const [fetching, isLoading, error] = useFetching(async () => {
    await service(data);
    setData({ working_time: getEmptySchedule(weekDays) });
    setShowMessage(true);
    messageTimeout(3000, setShowMessage);
  });

  const handleSubmit = (event) => {
    event.preventDefault();
    fetching();
  };

  return (
    <>
      {isLoading ? (
        <Loading />
      ) : (
        <Form
          formFields={formFields}
          formTitle={formTitle}
          data={data}
          setData={setData}
          handleSubmit={handleSubmit}
          error={error}
          showMessage={showMessage}
          messageText={messageText}
        />
      )}
    </>
  );
};

export default WorkingTimeForm;
