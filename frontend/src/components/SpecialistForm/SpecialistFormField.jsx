import { Typography, FormControl, FormHelperText, TextField } from '@mui/material';

const SpecialistFormField = ({ field, error, handler }) => {
  const isError = (fieldError) => !!error[fieldError.title];

  return (
    <div>
      {isError(field) && (
        <Typography component="p" variant="p" mb={2} color="error">
          {error[field.title]}
        </Typography>
      )}

      <FormControl sx={{ width: '100%' }}>
        <TextField
          id={field.title}
          label={field.title.toUpperCase().replace('_', ' ')}
          onChange={handler}
          type={field.type}
          variant="standard"
          error={isError(field)}
        />
        <FormHelperText error={isError(field)} id={`${field.title}-helper-text`}>
          {field.helpText}
        </FormHelperText>
      </FormControl>
    </div>
  );
};

export default SpecialistFormField;
