import { useState, useEffect } from 'react';
import './App.css';
import Navbar from './components/Navbar/Navbar';
import { BrowserRouter } from 'react-router-dom';
import AppRouter from './components/AppRouter';
import { AuthContext } from './context/index';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const authEmpty = { isAuth: false, user: {}, access: '', refresh: '' };
  const [auth, setAuth] = useState(authEmpty);

  useEffect(() => {
    const authData = JSON.parse(localStorage.getItem('auth'));
    if (authData != null) {
      setAuth(...authData);
    }
    setIsLoading(false);
  }, []);

  return (
    <AuthContext.Provider value={{ auth, setAuth, isLoading, setIsLoading, authEmpty }}>
      <BrowserRouter>
        <Navbar />
        <AppRouter />
      </BrowserRouter>
    </AuthContext.Provider>
  );
}

export default App;
