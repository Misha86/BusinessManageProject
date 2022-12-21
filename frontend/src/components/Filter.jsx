import React from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

const Filter = ({ fields, setData, data }) => {
  return (
    <Autocomplete
      id="filter-positions"
      onChange={(event, newValue) => setData(newValue)}
      value={data}
      options={fields}
      renderInput={(params) => <TextField {...params} variant="standard" label="Position filter" />}
    />
  );
};

export default Filter;
