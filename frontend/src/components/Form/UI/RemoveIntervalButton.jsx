import React from 'react';
import { IconButton, Icon } from '@mui/material';

const RemoveIntervalButton = ({ intervals, setIntervals, component: Component }) => {
  const removeInterval = (intervals, setIntervals) => {
    if (intervals.length >= 1) {
      intervals.pop();
      setIntervals([...intervals]);
    }
  };
  return (
    <>
      {intervals.length >= 1 && (
        <Component>
          <IconButton
            sx={{ padding: 0 }}
            aria-label="remove time interval"
            onClick={() => removeInterval(intervals, setIntervals)}
          >
            <Icon color="primary">do_not_disturb_on</Icon>
          </IconButton>
        </Component>
      )}
    </>
  );
};

export default RemoveIntervalButton;
