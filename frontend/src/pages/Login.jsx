import { Typography, Box } from '@mui/material';
import React from 'react';
import LoginForm from '../components/LoginForm';

const formFields = ['Email', 'Password'];

const Login = () => {
  return (
    <Box mt={3} sx={{ paddingLeft: '30%', width: '40%' }}>
      <Typography component="h5" variant="h5" mb={2} color="primary">
        Login
      </Typography>
      <LoginForm formFields={formFields} />
    </Box>
  );
};

export default Login;
