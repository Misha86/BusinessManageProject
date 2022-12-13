import React, { useState, useEffect } from 'react';
import Form from '../components/Form/Form';
import { ManagerService } from '../services/auth.service';
import { messageTimeout } from '../utils';

const AddSpecialist = () => {
  const [userData, setUserData] = useState({});
  const [error, setError] = useState({});
  const [showMessage, setShowMessage] = useState(false);
  const [formFields, setFormFields] = useState([]);

  useEffect(() => {
    const getFieldsInfo = async () => {
      await ManagerService.getSpecialistFieldsOption()
        .then((response) => {
          const fields = response.data.fields;
          fields['bio']['type'] = 'textarea';
          setFormFields(fields);
        })
        .catch((error) => {
          console.log(error.response.data);
        });
    };
    getFieldsInfo();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await ManagerService.addSpecialist(userData);
      setUserData({});
      setError({});
      setShowMessage(true);
      messageTimeout(7000, setShowMessage);
    } catch (error) {
      console.log(error.response.data);
      setError(error.response.data);
    }
  };

  return (
    <Form
      formFields={formFields}
      formTitle="Add Specialist"
      data={userData}
      setData={setUserData}
      handleSubmit={handleSubmit}
      error={error}
      showMessage={showMessage}
    />
  );
};

export default AddSpecialist;
