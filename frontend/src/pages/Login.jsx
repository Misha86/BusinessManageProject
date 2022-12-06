import React, { useState, useContext } from 'react';
import Form from '../components/Form/Form';
import { useNavigate } from 'react-router-dom';
import { AuthService } from '../services/auth.service';
import { AuthContext } from '../context/index';

const formFields = [
  { title: 'email', type: 'email', required: true, helpText: "We'll never share your email" },
  { title: 'password', type: 'password', required: true, helpText: "We'll never share your password" },
];

const Login = () => {
  const [userData, setUserData] = useState({});
  const [error, setError] = useState('');
  const { setAuth } = useContext(AuthContext);

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
    />
  );
};

export default Login;
