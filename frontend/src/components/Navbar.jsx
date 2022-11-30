import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import MenuItem from '@mui/material/MenuItem';
import AdbIcon from '@mui/icons-material/Adb';
import { Link } from 'react-router-dom';

const pages = [
  { title: 'Add Specialist', sxStyle: {}, path: '/add-specialist' },
  { title: 'Add Schedule', sxStyle: {}, path: '/add-schedule' },
  { title: 'Add Location', sxStyle: {}, path: '/add-location' },
  { title: 'Login', sxStyle: { marginLeft: 'auto' }, path: '/login' },
];

const Navbar = () => {
  return (
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <AdbIcon sx={{ display: { xs: 'none', md: 'flex' } }} />
          <Typography
            variant="h6"
            noWrap
            component={Link}
            to="/"
            sx={{
              mr: 2,
              display: { md: 'flex' },
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            LOGO
          </Typography>
          {pages.map((page) => (
            <MenuItem sx={page.sxStyle} component={Link} to={page.path} key={page.title}>
              <Typography component="h6" textAlign="center" variant="h6">
                {page.title}
              </Typography>
            </MenuItem>
          ))}
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar;
