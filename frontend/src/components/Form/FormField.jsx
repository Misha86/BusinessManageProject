import { FormControl, FormHelperText, TextField } from '@mui/material';
import ErrorField from './ErrorField';

const FormField = ({ fieldTitle, fieldInfo, errorMessage, handler, type, value, multiline }) => {

  const fileProps = { accept: 'image/png, image/jpeg' };

  return (
    <div>

      <ErrorField errorMessage={errorMessage}/>

      <FormControl sx={{ width: '100%' }}>
        <TextField
          id={fieldTitle}
          label={fieldInfo.label}
          required={fieldInfo.required}
          inputProps={fileProps}
          onChange={handler}
          type={type || 'text'}
          variant="standard"
          size="small"
          error={!!errorMessage}
          value={value}
          rows="4"
          multiline={multiline}
        />
        <FormHelperText error={!!errorMessage} id={`${fieldTitle}-helper-text`}>
          {fieldInfo.help_text}
        </FormHelperText>
      </FormControl>
    </div>
  );
};

export default FormField;
