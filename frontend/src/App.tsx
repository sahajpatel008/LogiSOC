import Navbar from './components/Navbar.tsx';
import Dashboard from './pages/Dashboard.tsx'
import './App.css';
import { SignedIn } from "@clerk/clerk-react";
import Box from '@mui/material/Box';

function App() {

  return (
    <>
      <Navbar />

      <SignedIn>
        <Box sx={{ pt: 2 }}>
          <Dashboard />
        </Box>
      </SignedIn>

    </>
  )
}

export default App
