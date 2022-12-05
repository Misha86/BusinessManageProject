import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Paper } from '@mui/material';
import { ManagerService } from '../../services/auth.service';
import SpecialistFormField from './SpecialistFormField';
import { useCookies } from 'react-cookie';


const AddSpecialistForm = ({ formFields }) => {
  const [userData, setUserData] = useState({});

  const [error, setError] = useState({});

  const [cookies, setCookie] = useCookies();

  const router = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await ManagerService.addSpecialist(userData, cookies.csrftoken);
      router('/');
    } catch (error) {
      console.log(error.response.data);
      setError(error.response.data);
    }
  };

  const handleTextInput = (event) => {
    const textValue = event.target.value;
    setUserData({ ...userData, [event.target.id]: textValue });
  };

  const handleFileInput = (event) => {
    const fileValue = event.target.files[0];
    setUserData({ ...userData, [event.target.id]: fileValue });
  };

  const chooseInputHandler = (event) => {
    event.target.type === 'file' ? handleFileInput(event) : handleTextInput(event);
  };

  return (
    <form onSubmit={handleSubmit}>
      <Paper elevation={3} sx={{ padding: '6%' }}>
        {formFields.map((field) => (
          <SpecialistFormField
            key={field.title}
            field={field}
            error={error}
            handler={chooseInputHandler}
          />
        ))}
        <Button variant="contained" color="primary" type="submit">
          Add
        </Button>
      </Paper>
    </form>
  );
};

export default AddSpecialistForm;
