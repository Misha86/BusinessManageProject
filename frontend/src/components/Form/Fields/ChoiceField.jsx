import React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import FormHelperText from '@mui/material/FormHelperText';
import ErrorField from '../ErrorField';

const ChoiceField = ({ fieldTitle, fieldInfo, errorMessage, handler , value}) => {

  return (
    <div>

      <ErrorField errorMessage={errorMessage}/>

      <FormControl variant="standard" sx={{ minWidth: '100%' }}>
        <InputLabel id={`${fieldInfo.label}-standard-label`}>{fieldInfo.label}</InputLabel>
        <Select
          labelId={`${fieldInfo.label}-standard-label`}
          id={fieldTitle}
          value={value}
          onChange={(e) => handler(e, fieldTitle)}
          label={fieldInfo.label}
          required={fieldInfo.required}
          error={!!errorMessage}
        >
          {fieldInfo.choices.map((variant) => (
            <MenuItem id={`${fieldTitle}-${variant.value}`} key={variant.value} value={variant.value}>
              {variant.display_name}
            </MenuItem>
          ))}
        </Select>
        <FormHelperText id={`${fieldTitle}-helper-text`} error={!!errorMessage}>
          {fieldInfo.help_text}
        </FormHelperText>
      </FormControl>
    </div>
  );
};

export default ChoiceField;
