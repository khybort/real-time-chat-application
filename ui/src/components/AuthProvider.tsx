import { jwtDecode } from 'jwt-decode';
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

interface AuthProviderProps {
  children: React.ReactNode;
}

const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('access');
    const currentPath = window.location.pathname;

    if (currentPath === '/login' || currentPath === '/register') {
      return;
    }

    if (!token) {
      navigate('/login');
      return;
    }

    try {
      const decoded: any = jwtDecode(token);
      const expiration = decoded.exp * 1000;
      const currentTime = Date.now();

      if (currentTime >= expiration) {
        localStorage.removeItem('access');
        navigate('/login');
      } else if (currentPath === '/') {
        navigate('/chat');
      }
    } catch (error) {
      localStorage.removeItem('access');
      navigate('/login');
    }
  }, [navigate]);

  return <>{children}</>;
};

export default AuthProvider;
