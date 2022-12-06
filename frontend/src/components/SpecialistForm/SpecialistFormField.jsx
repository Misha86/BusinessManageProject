import { Typography, FormControl, FormHelperText, TextField } from '@mui/material';

const SpecialistFormField = ({ field, error, handler }) => {
  const isError = (fieldError) => !!error[fieldError.title];

  const fieldLabel = (field) => {
    let fieldTitle = field.title[0].toUpperCase() + field.title.slice(1);
    return fieldTitle.replace('_', ' ');
  };

  const fieldAttrs = {
    textarea: { multiline: true, rows: 4 },
    file: { accept: 'image/png, image/jpeg' },
  };

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
          label={fieldLabel(field)}
          required={field.required}
          onChange={handler}
          type={field.type}
          variant="standard"
          size="small"
          error={isError(field)}
          {...fieldAttrs[field.type]}
        />
        <FormHelperText error={isError(field)} id={`${field.title}-helper-text`}>
          {field.helpText}
        </FormHelperText>
      </FormControl>
    </div>
  );
};

export default SpecialistFormField;
