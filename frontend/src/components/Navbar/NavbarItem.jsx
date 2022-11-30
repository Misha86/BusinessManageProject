import React from 'react';
import Typography from '@mui/material/Typography';
import MenuItem from '@mui/material/MenuItem';
import { Link } from 'react-router-dom';


const NavbarItem = ({page}) => {
  return (
    <MenuItem sx={page.sxStyle} component={Link} to={page.path}>
      <Typography component="h6" textAlign="center" variant="h6">
        {page.title}
      </Typography>
    </MenuItem>
  );
};


export default NavbarItem;
