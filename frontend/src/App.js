import { useState, useEffect } from 'react';
import './App.css';
import Navbar from './components/Navbar/Navbar';
import { BrowserRouter } from 'react-router-dom';
import AppRouter from './components/AppRouter';
import { AuthContext } from './context/index';
import { AuthService } from './services/auth.service';
import { ThemeProvider } from '@mui/material/styles';
import {customTheme} from './themes/themes'


function App() {
  const [isLoading, setIsLoading] = useState(true);
  const authEmpty = { user: {}, access: '', refresh: '' };
  const [auth, setAuth] = useState(authEmpty);

  useEffect(() => {
    const authData = AuthService.getAuthData();
    if (authData) {
      setAuth(authData);
    }
    setIsLoading(false);
  }, []);

  return (
    <AuthContext.Provider value={{ auth, setAuth, isLoading, setIsLoading, authEmpty }}>
      <BrowserRouter>
        <ThemeProvider theme={customTheme}>
          <Navbar />
          <AppRouter />
        </ThemeProvider>
      </BrowserRouter>
    </AuthContext.Provider>
  );
}

export default App;
