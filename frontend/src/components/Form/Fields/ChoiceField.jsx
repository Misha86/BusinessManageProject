import React, { useState, useEffect, useMemo } from 'react';
import FormControl from '@mui/material/FormControl';
import FormHelperText from '@mui/material/FormHelperText';
import ErrorField from '../ErrorField';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

const ChoiceField = ({ fieldTitle, fieldInfo, errorMessage, data, setData }) => {
  const [value, setValue] = useState(null);

  const id = useMemo(() => {
    return value ? value.value : '';
  }, [value]);

  useEffect(() => {
    value && setData({ ...data, [fieldTitle]: id });
  }, [id]);

  return (
    <div>
      <ErrorField errorMessage={errorMessage} />

      <FormControl variant="standard" sx={{ minWidth: '100%' }}>
        <Autocomplete
          id="filter-positions"
          value={fieldInfo.choices.filter((item) => item.value === data[fieldTitle])[0] || null}
          onChange={(_event, newValue) => {
            setValue(newValue);
          }}
          getOptionLabel={(option) => option.display_name}
          options={fieldInfo.choices}
          renderInput={(params) => (
            <TextField
              {...params}
              error={!!errorMessage}
              required={fieldInfo.required}
              variant="standard"
              label={fieldInfo.label}
            />
          )}
        />

        <FormHelperText id={`${fieldTitle}-helper-text`} error={!!errorMessage}>
          {fieldInfo.help_text}
        </FormHelperText>
      </FormControl>
    </div>
  );
};

export default ChoiceField;
