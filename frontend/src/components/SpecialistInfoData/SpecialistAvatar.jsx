import React from 'react';
import { Paper } from '@mui/material';
import { Image } from 'mui-image';

const SpecialistAvatar = ({avatar, alt}) => {
  return (
    <Paper elevation={3}>
      <Image src={avatar} alt={alt} showLoading shift="top" distance={300} />
    </Paper>
  );
};

export default SpecialistAvatar;
