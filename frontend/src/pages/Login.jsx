import { Input, Typography, Button, Box, FormControl, InputLabel, FormHelperText, Paper } from '@mui/material';
import React from 'react';

const formFields = ['Email', 'Password']

const Login = () => {
  return (
    <Box mt={3} sx={{ paddingLeft: '30%', width: '40%' }}>
      <Typography component="h5" variant="h5" mb={2} color="primary">
        Login
      </Typography>
      <form>
        <Paper elevation={3} sx={{ padding: '6%'}}>
          {formFields.map((field) => (
            <FormControl sx={{ width: '100%' }}>
              <InputLabel htmlFor={field}>{field} address</InputLabel>
              <Input id={field} aria-describedby={`${field}-helper-text`} type={field} required />
              <FormHelperText id={`${field}-helper-text`}>We'll never share your {field}.</FormHelperText>
            </FormControl>
          ))}
          <Button variant="contained" color="primary" type="submit">
            Login
          </Button>
        </Paper>
      </form>
    </Box>
  );
};

export default Login;
