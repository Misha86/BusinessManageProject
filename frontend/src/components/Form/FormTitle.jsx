import React from 'react';
import { Typography } from '@mui/material';

const FormTitle = ({ formTitle, props }) => {
  return (
    <Typography {...props} component="h5" variant="h5" color="primary">
      {formTitle}
    </Typography>
  );
};

export default FormTitle;
