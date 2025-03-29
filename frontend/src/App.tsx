import { useState } from 'react'
import Navbar from './components/Navbar.tsx';
import PieChartComponent from './components/PieChart.tsx';
import CustomTable from './components/Table.tsx';
import Dashboard from './pages/Dashboard.tsx'
import './App.css';
import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react";
import Box from '@mui/material/Box';

function App() {

  return (
    <>
      <header>
        <SignedOut>
          <SignInButton />
        </SignedOut>
        <SignedIn>
          <UserButton />
          <Box sx={{ pt: 10 }}> {/* add padding to push content below the navbar */}
            <Dashboard />
          </Box>
        </SignedIn>
      </header>
      <Navbar />
      {/* <PieChartComponent></PieChartComponent>
      <CustomTable></CustomTable> */}

    </>
  )
}

export default App
