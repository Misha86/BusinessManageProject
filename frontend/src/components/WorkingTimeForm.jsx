import React, { useState, useEffect } from 'react';
import { getEmptySchedule, messageTimeout } from '../utils';
import { weekDays } from '../utils';
import Form from './Form/Form';
import useFetching from '../hooks/useFetching';
import Loading from './Loading';

const WorkingTimeForm = ({ formTitle, service, messageText, setCreated, created, serviceFields }) => {
  const [data, setData] = useState({ working_time: getEmptySchedule(weekDays) });
  const [showMessage, setShowMessage] = useState(false);
  const [formFields, setFormFields] = useState([]);
  const [fetching, isLoading, error] = useFetching(async () => {
    await service(data);
    setCreated(true);
    setData({ working_time: getEmptySchedule(weekDays) });
    setShowMessage(true);
    messageTimeout(7000, setShowMessage);
  });

  useEffect(() => {
    const getFieldsInfo = async () => {
      await serviceFields()
        .then((response) => {
          setFormFields(response.data.fields);
        })
        .catch((error) => {
          console.log(error.response.data);
        });
    };
    getFieldsInfo();
  }, [created]);

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
