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
      <Navbar />

      <SignedIn>
        <Box sx={{ pt: 10 }}>
          <Dashboard />
        </Box>
      </SignedIn>

    </>
  )
}

export default App
