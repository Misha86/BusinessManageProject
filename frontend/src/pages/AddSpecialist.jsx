import { Input, Typography, Button } from '@mui/material';
import { Box } from '@mui/system';
import React from 'react';
import { Form } from 'react-router-dom';

const AddSpecialist = () => {
  return (
    <Box>
      <Typography>Login</Typography>
      <form>
        <Input />
        <Input />
        <Button>Submit</Button>
      </form>
    </Box>
  );
};

export default AddSpecialist;
