import React from 'react';
import { Typography } from '@mui/material';

const ErrorDetail = ({ error, props }) => {
  return (
    <>
      {error && error.detail && (
        <Typography {...props} component="p" variant="p" mb={2} color="error">
          {error.detail}
        </Typography>
      )}
    </>
  );
};

export default ErrorDetail;
