import React from 'react';
import { Typography } from '@mui/material';

const ErrorDetail = ({ errorMessage }) => {
  return (
    <>
      {!!errorMessage && (
        <Typography component="p" variant="p" mb={2} color="error">
          {errorMessage}
        </Typography>
      )}
    </>
  );
};

export default ErrorDetail;
