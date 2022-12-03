import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Input, Typography, Button, FormControl, InputLabel, FormHelperText, Paper } from '@mui/material';
import UserService from '../services/UserService';
import { AuthContext } from '../context/index';
import { useContext } from 'react';

const LoginForm = ({ formFields }) => {
  const [userData, setUserData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const { setIsAuth, setAuth } = useContext(AuthContext);

  const router = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await UserService.login(userData);
      localStorage.setItem('token', response.data.access);
      localStorage.setItem('auth', JSON.stringify(response.data.user));
      setAuth(response.data.user);
      setIsAuth(true);
      router('/');
    } catch (error) {
      console.log(error);
      setError(error.response.data.detail);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Paper elevation={3} sx={{ padding: '6%' }}>
        {error && (
          <Typography component="p" variant="p" mb={2} color="red">
            {error}
          </Typography>
        )}

        {formFields.map((field) => (
          <FormControl sx={{ width: '100%' }} key={field}>
            <InputLabel htmlFor={field}>{field} address</InputLabel>
            <Input
              id={field}
              aria-describedby={`${field}-helper-text`}
              type={field}
              required
              value={userData[`${field}`]}
              onChange={(e) => setUserData({ ...userData, [field.toLowerCase()]: e.target.value })}
            />
            <FormHelperText id={`${field}-helper-text`}>We'll never share your {field}.</FormHelperText>
          </FormControl>
        ))}
        <Button variant="contained" color="primary" type="submit">
          Login
        </Button>
      </Paper>
    </form>
  );
};

export default LoginForm;
