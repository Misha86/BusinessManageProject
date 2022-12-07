import React from 'react';
import { Fade, Typography } from '@mui/material';

const Message = ({ showMessage, messageText }) => {
  return (
    <Fade appear={false} in={showMessage} timeout={{ appear: 5000, enter: 5000, exit: 5000 }}>
      <Typography component="h6" variant="h6" color="green">
        {messageText}
      </Typography>
    </Fade>
  );
};

export default Message;
