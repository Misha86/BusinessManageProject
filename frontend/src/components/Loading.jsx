import React from 'react';
import { Typography, Box } from '@mui/material';

const Loading = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
      }}
    >
      <Typography component="p" variant="p" pt={'30%'}>
        Loading...
      </Typography>
    </Box>
  );
};

export default Loading;
