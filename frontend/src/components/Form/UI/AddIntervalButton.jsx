import React from 'react';
import { IconButton, Icon } from '@mui/material';

const AddIntervalButton = ({ intervals, setIntervals, count, component: Component }) => {
  const addInterval = (intervals, setIntervals, count) => {
    if (intervals.length < count) {
      setIntervals([...intervals, []]);
    }
  };

  return (
    <>
      {intervals.length < count && (
        <Component>
          <IconButton 
            sx={{ padding: 0 }}
            aria-label="add time interval"
            onClick={() => addInterval(intervals, setIntervals, count)}
          >
            <Icon color="primary">add_circle</Icon>
          </IconButton>
        </Component>
      )}
    </>
  );
};

export default AddIntervalButton;
