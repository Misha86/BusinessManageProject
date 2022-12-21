import React from 'react';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import NativeSelect from '@mui/material/NativeSelect';

const SelectForm = ({ defaultValue, optionArray, setData, label }) => {
  return (
    <FormControl fullWidth onChange={e => setData(e.target.value)}>
      <InputLabel variant="standard" htmlFor="uncontrolled-native">
        {label}
      </InputLabel>
      <NativeSelect
        defaultValue={defaultValue}
        inputProps={{
          name: `${label}`,
          id: 'uncontrolled-native',
        }}
      >
        {optionArray.map((value) => (
          <option key={value} value={value[0]}>
            {value[1]}
          </option>
        ))}
      </NativeSelect>
    </FormControl>
  );
};

export default SelectForm;
