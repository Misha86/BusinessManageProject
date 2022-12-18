import React, { useEffect, useState } from 'react';
import { getEmptySchedule, messageTimeout } from '../utils';
import { weekDays } from '../utils';
import Form from './Form/Form';
import useFetching from '../hooks/useFetching';
import Loading from './Loading';

const WorkingTimeForm = ({ formTitle, service, messageText, serviceFields }) => {
  const [data, setData] = useState({ working_time: getEmptySchedule(weekDays) });
  const [showMessage, setShowMessage] = useState(false);
  const [created, setCreated] = useState(false);
  const [formFields, setFormFields] = useState([]);

  const [fetching, isLoading, error] = useFetching(async () => {
    await service(data);
    setCreated(true);
    setShowMessage(true);
    setData({ working_time: getEmptySchedule(weekDays) });
    messageTimeout(3000, setShowMessage);
  });

  const [fetchingFields, isLoadingFields] = useFetching(async () => {
    const response = await serviceFields();
    setFormFields(response.data.fields);
  });

  useEffect(() => {
    fetchingFields();
    setCreated(false);
  }, [created]);

  const handleSubmit = (event) => {
    event.preventDefault();
    fetching();
  };

  return (
    <>
      {isLoading || isLoadingFields ? (
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
