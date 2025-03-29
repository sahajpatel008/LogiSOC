// src/components/Navbar.jsx
import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { SignedIn, SignedOut, SignInButton, UserButton, useUser } from "@clerk/clerk-react";
import { Link } from 'react-router-dom';



const Navbar = () => {
  const { user } = useUser();

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="fixed" color="primary" elevation={2}>
        <Toolbar sx={{ justifyContent: "space-between" }}>
        <Typography variant="h6" component={Link} to="/" sx={{ color: 'inherit', textDecoration: 'none' }}>
            LogiSOC
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <SignedOut>
              <SignInButton mode="modal" />
            </SignedOut>
            <SignedIn>
              <Typography variant="body1" sx={{ display: { xs: 'none', sm: 'block' } }}>
                {user?.fullName || user?.username || 'User'}
              </Typography>
              <UserButton afterSignOutUrl="/" />
            </SignedIn>
          </Box>
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default Navbar;
