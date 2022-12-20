import React from 'react';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import NativeSelect from '@mui/material/NativeSelect';

const PageSizeForm = ({ pageSize, optionArray, setPageSize }) => {
  const handlePageSize = (event) => {
    setPageSize(event.target.value);
  };

  return (
    <FormControl fullWidth onChange={handlePageSize}>
      <InputLabel variant="standard" htmlFor="uncontrolled-native">
        Items
      </InputLabel>
      <NativeSelect
        defaultValue={pageSize}
        inputProps={{
          name: 'items',
          id: 'uncontrolled-native',
        }}
      >
        {optionArray.map((value) => (
          <option key={value} value={value}>
            {value}
          </option>
        ))}
      </NativeSelect>
    </FormControl>
  );
};

export default PageSizeForm;
