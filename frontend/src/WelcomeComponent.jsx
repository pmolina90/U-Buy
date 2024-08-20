import React, { useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const WelcomeComponent = () => {
  const { loginWithRedirect, isAuthenticated, getIdTokenClaims } = useAuth0();
  const navigate = useNavigate();

  useEffect(() => {
    const handleAuthentication = async () => {
      if (isAuthenticated) {
        try {
          const idToken = await getIdTokenClaims();
          const token = idToken.__raw;

          // Send the ID token to your Django backend
          const response = await axios.post('http://127.0.0.1:8000/api/token/', {
            token
          });

          // Extract and store the JWT tokens from your backend response
          const { access, refresh } = response.data;
          localStorage.setItem('access_token', access);
          localStorage.setItem('refresh_token', refresh);

          // Redirect to the store page after successful login and token exchange
          navigate('/store');
        } catch (error) {
          console.error('Error during authentication:', error);
        }
      }
    };

    handleAuthentication();
  }, [isAuthenticated, getIdTokenClaims, navigate]);

  const handleLogin = () => {
    loginWithRedirect({ prompt: 'login select_account' });
  };

  return (
    <div className="welcome-container">
      <h1 className="welcome-text">Welcome</h1>
      <button className="welcome-button" onClick={handleLogin}>
        X-clusive Access
      </button>
    </div>
  );
};

export default WelcomeComponent;