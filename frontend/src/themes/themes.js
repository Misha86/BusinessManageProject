import { createTheme } from '@mui/material/styles';

export const customTheme = createTheme({
  palette: {
    primary: {
      main: '#0288d1',
    },
    secondary: {
      main: '#651fff',
    },
  }
});


customTheme.typography.p = {
  fontFamily: 'Roboto, Helvetica, Arial',
  color: 'gray'
};