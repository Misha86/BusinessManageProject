import React, { useContext } from 'react';
import Typography from '@mui/material/Typography';
import MenuItem from '@mui/material/MenuItem';
import { Link } from 'react-router-dom';
import { AuthContext } from '../../context';

const NavbarItem = (props) => {
  const { setIsAuth, setAuth } = useContext(AuthContext);

  const logOut = () => {
    setIsAuth(false);
    localStorage.clear();
    setAuth({});
  };

  if (props.title === 'Logout') {
    props = { ...props, onClick: logOut };
  }

  return (
    <MenuItem {...props} component={Link}>
      <Typography component="h6" textAlign="center" variant="h6">
        {props.title}
      </Typography>
    </MenuItem>
  );
};

export default NavbarItem;
