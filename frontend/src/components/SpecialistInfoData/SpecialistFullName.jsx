import React from 'react';
import {  Typography } from '@mui/material';


const SpecialistFullName = ({fullName}) => {
  return (
    <Typography gutterBottom variant="h5" component="h5" color="gray">
    {fullName}
  </Typography>
  )
}

export default SpecialistFullName