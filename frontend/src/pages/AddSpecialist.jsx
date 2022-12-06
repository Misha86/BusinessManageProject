import React, { useState } from 'react';
import Form from '../components/Form/Form';
import { useNavigate } from 'react-router-dom';
import { ManagerService } from '../services/auth.service';

const formFields = [
  { title: 'email', type: 'email', required: true, helpText: 'This field is required' },
  { title: 'first_name', type: 'text', required: true, helpText: 'This field is required' },
  { title: 'last_name', type: 'text', required: true, helpText: 'This field is required' },
  { title: 'patronymic', type: 'text', required: true, helpText: 'This field is not required' },
  { title: 'position', type: 'text', required: true, helpText: 'This field is required' },
  { title: 'bio', type: 'textarea', required: false, helpText: 'This field is not required' },
  { title: 'avatar', type: 'file', required: false, helpText: 'Get Avatar to the profile' },
];

const AddSpecialist = () => {
  const [userData, setUserData] = useState({});
  const [error, setError] = useState({});
  const router = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await ManagerService.addSpecialist(userData);
      router('/');
    } catch (error) {
      console.log(error.response.data);
      setError(error.response.data);
    }
  };
  return (
    <Form
      formFields={formFields}
      formTitle="Add specialist"
      data={userData}
      setData={setUserData}
      handleSubmit={handleSubmit}
      error={error}
    />
  );
};

export default AddSpecialist;
