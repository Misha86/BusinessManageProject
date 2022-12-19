import React from 'react';
import { Typography, Box } from '@mui/material';

const Loader = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
      }}
    >
      <Typography component="p" variant="p" pt={'20%'}>
        Loading...
      </Typography>
    </Box>
  );
};

export default Loader;
