import React, { useState, useContext, useEffect } from 'react';
import Form from '../components/Form/Form';
import { useNavigate } from 'react-router-dom';
import { AuthService } from '../services/auth.service';
import { AuthContext } from '../context/index';

const Login = () => {
  const [userData, setUserData] = useState({});
  const [error, setError] = useState('');
  const { setAuth } = useContext(AuthContext);
  const [formFields, setFormFields] = useState([]);

  useEffect(() => {
    const getFieldsInfo = async () => {
      await AuthService.getLoginFieldsOption()
        .then((response) => {
          setFormFields(response.data.fields);
        })
        .catch((error) => {
          console.log(error.response.data);
        });
    };
    getFieldsInfo();
  }, []);

  const router = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await AuthService.login(userData);
      setAuth(response.data);
      router('/');
    } catch (error) {
      console.log(error.response.data);
      setError(error.response.data);
    }
  };

  return (
    <Form
      formFields={formFields}
      data={userData}
      setData={setUserData}
      handleSubmit={handleSubmit}
      error={error}
      formTitle="Login"
      messageText="Success login!"
    />
  );
};

export default Login;
