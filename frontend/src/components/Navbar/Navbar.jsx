import React, { useContext, useEffect, useState } from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import AdbIcon from '@mui/icons-material/Adb';
import { Link } from 'react-router-dom';
import { managerLinks, adminLinks, loginLinks } from './NavBarLinks';
import NavbarItem from './NavbarItem';
import { AuthContext } from '../../context';

const Navbar = () => {
  const [pages, setPages] = useState([]);
  const { auth, isLoading } = useContext(AuthContext);
  const {isAuth, user, ...rest} = auth

  useEffect(() => {
    const getLinks = async () => {
      if (!isLoading) {
        if (isAuth && user.groups.includes('Manager')) {
          setPages(managerLinks);
        } else if (isAuth && user.groups.includes('Admin')) {
          setPages(adminLinks);
        } else {
          setPages(loginLinks);
        }
      }
    };
    getLinks();
  }, [auth, isLoading]);

  return (
    <>
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
              <NavbarItem {...page} key={page.title} />
            ))}
            <NavbarItem page={0} />
          </Toolbar>
        </Container>
      </AppBar>
    </>
  );
};

export default Navbar;
