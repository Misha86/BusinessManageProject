import React from 'react';
import { Typography } from '@mui/material';

const ErrorField = ({ errorMessage }) => {
  return (
    <>
      {!!errorMessage && (
        <Typography component="p" variant="p" mb={2}  mt={1} color="error">
          {errorMessage}
        </Typography>
      )}
    </>
  );
};

export default ErrorField;
