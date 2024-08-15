// src/WelcomeComponent.jsx
import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';

const WelcomeComponent = () => {
  const { loginWithRedirect } = useAuth0();

  const handleLogin = () => {
    loginWithRedirect({prompt: 'login select_account'});
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