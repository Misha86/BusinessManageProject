import { Input, Typography, FormControl, InputLabel, FormHelperText, TextField } from '@mui/material';

const SpecialistFormField = ({ field, error, handler }) => {
  const isError = (fieldError) => !!error[fieldError.title];

  return (
    <div>
      {isError(field) && (
        <Typography component="p" variant="p" mb={2} color="red">
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


//   return (
//     <div>
//       {isError(field) && (
//         <Typography component="p" variant="p" mb={2} color="red">
//           {error[field.title]}
//         </Typography>
//       )}

//       <FormControl sx={{ width: '100%' }}>
//         {field.type !== 'file' && (
//           <InputLabel error={isError(field)} htmlFor={field.title}>
//             {field.title.toUpperCase().replace('_', ' ')}
//           </InputLabel>
//         )}
//         <Input
//           id={field.title}
//           error={isError(field)}
//           aria-describedby={`${field.title}-helper-text`}
//           type={field.type}
//           required={field.required}
//           // value={userData[`${field.title}`]}
//           onChange={handler}
//         />
//         <FormHelperText error={isError(field)} id={`${field}-helper-text`}>
//           {field.helpText}
//         </FormHelperText>
//       </FormControl>
//     </div>
//   );
// };

export default SpecialistFormField;
