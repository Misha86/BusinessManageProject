import { Input, Typography, Button, Container, Box } from '@mui/material';
import React from 'react';

const Login = () => {
  return (
    <Container>
      <Box mt={3} sx={{paddingLeft: '25%', width: '50%'}}>
        <Typography component="h6" variant="h6">
          Login
        </Typography>
        <form>
          <input type="text" placeholder="Input email" />
          <input type="password" placeholder="Input password" />
          <Button>Send Request</Button>
        </form>
      </Box>
    </Container>
  );
};

export default Login;
