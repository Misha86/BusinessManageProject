import React, { useState, useEffect } from 'react';
import Form from '../components/Form/Form';
import { ManagerService } from '../services/auth.service';
import { messageTimeout } from '../utils';
import useFetching from '../hooks/useFetching';
import Loader from '../components/Loader';

const AddSpecialist = () => {
  const [userData, setUserData] = useState({});
  const [showMessage, setShowMessage] = useState(false);
  const [formFields, setFormFields] = useState([]);
  const [fetching, isLoading, error] = useFetching(async () => {
    await ManagerService.addSpecialist(userData);
    setShowMessage(true);
    setUserData({});
    messageTimeout(3000, setShowMessage);
  });

  const [fetchingFields, isLoadingFields] = useFetching(async () => {
    const response = await ManagerService.getSpecialistFieldsOption();
    const fields = response.data.fields;
    fields['bio']['type'] = 'textarea';
    setFormFields(fields);
  });

  useEffect(() => {
    fetchingFields();
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    fetching();
  };

  return (
    <>
      {isLoading || isLoadingFields ? (
        <Loader />
      ) : (
        <Form
          formFields={formFields}
          formTitle="Add Specialist"
          data={userData}
          setData={setUserData}
          handleSubmit={handleSubmit}
          error={error}
          showMessage={showMessage}
          messageText="The specialist was added!"
        />
      )}
    </>
  );
};

export default AddSpecialist;
