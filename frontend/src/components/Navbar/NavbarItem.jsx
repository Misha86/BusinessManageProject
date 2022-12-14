import React, { useContext } from 'react';
import Typography from '@mui/material/Typography';
import MenuItem from '@mui/material/MenuItem';
import { Link } from 'react-router-dom';
import { AuthContext } from '../../context';
import { useNavigate } from 'react-router-dom';
import { AuthService } from '../../services/auth.service';

const NavbarItem = (props) => {
  const { auth, setAuth, authEmpty } = useContext(AuthContext);
  const router = useNavigate();
  const { refresh, user } = auth;

  const logOut = async () => {
    try {
      await AuthService.logOut(refresh);
      setAuth({ authEmpty });
      router('/');
    } catch (err) {
      console.log(err);
      console.log(err.response.status);
    }
  };

  if (props.title === 'Logout' && user) {

    props = { ...props, onClick: logOut, title: `(${user.first_name} ${user.last_name}) Logout` };
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
