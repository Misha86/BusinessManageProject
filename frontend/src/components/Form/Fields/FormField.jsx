import { FormControl, FormHelperText, TextField } from '@mui/material';
import ErrorField from '../ErrorField';

const FormField = ({ fieldTitle, fieldInfo, errorMessage, handler, type, value, multiline, props }) => {
  const fileProps = { accept: 'image/png, image/jpeg' };

  return (
    <div>
      <ErrorField errorMessage={errorMessage} />

      <FormControl sx={{ width: '100%' }}>
        <TextField
          id={fieldTitle}
          label={fieldInfo.label}
          required={fieldInfo.required}
          inputProps={fileProps}
          onChange={(e) => {
            handler(e, fieldTitle, type);
          }}
          type={type || 'text'}
          variant="standard"
          size="small"
          error={!!errorMessage}
          value={value}
          rows="4"
          multiline={multiline}
          {...props}
        />
      </FormControl>
      <FormHelperText error={!!errorMessage} id={`${fieldTitle}-helper-text`}>
        {fieldInfo.help_text}
      </FormHelperText>
    </div>
  );
};

export default FormField;
