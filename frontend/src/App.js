import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';
import './App.css';
import WelcomeComponent from './WelcomeComponent'; // Import the new component
import StoreComponent from './StoreComponent';
import AdminComponent from './adminComponent';
import LoginComponent from './LoginComponent';
import './WelcomeComponent.css'; // Import the CSS for the new component
import { logout as authLogout } from './auth';

const PrivateRoute = ({ element, roles }) => {
  const { isAuthenticated , user, isLoading} = useAuth0();
  const namespace = 'http://get_roles.net';
  const userRoles = user ? user[`${namespace}/role`] : null;

  if (isLoading) {
    return <div>Loading...</div>; // Show a loading message while user data is being fetched
  }

  console.log('isAuthenticated:', isAuthenticated);
  console.log('user:', user);
  console.log('userRole:', userRoles);

  if (!isAuthenticated) {
    console.log('User is not authenticated, redirecting to /');
    return <Navigate to="/" />;
  }

  if (!roles.some(role => userRoles.includes(role))) {
    console.log(`User role ${userRoles} is not authorized, redirecting to /`);
    return <Navigate to="/" />;
  }

  return element;
};

function App() {
  const { isAuthenticated, user, logout: auth0Logout, isLoading } = useAuth0();
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('access_token'));

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    authLogout(); // Call the logout function from Auth.js
    auth0Logout({ returnTo: window.location.origin });
    setIsLoggedIn(false); // Update the state to reflect the logout
  };

  if (isLoading) {
    return <div>Loading...</div>; // Show a loading message while authentication data is being fetched
  }

  return (
    <Router>
      <div>
        {isAuthenticated ? (
          <>
            <p>Welcome, {user.name}!</p>
            <button onClick={handleLogout}>
              Log Out
            </button>
            <Routes>
              <Route path="/store" element={<PrivateRoute roles={['User', 'Admin']} element={<StoreComponent />} />} />
              <Route path="/admin" element={<PrivateRoute roles={['Admin']} element={<AdminComponent />} />} />
              <Route path="*" element={<Navigate to="/store" />} />
            </Routes>
          </>
        ) : (
          <>
            {isLoggedIn ? (
              <Routes>
                <Route path="/store" element={<StoreComponent />} />
                <Route path="*" element={<Navigate to="/store" />} />
              </Routes>
            ) : (
              <>
                <WelcomeComponent />
                <Routes>
                  <Route path="/" element={<WelcomeComponent />} />
                  <Route path="/login" element={<LoginComponent onLoginSuccess={handleLoginSuccess} />} />
                  <Route path="*" element={<Navigate to="/" />} />
                </Routes>
              </>
            )}
          </>
        )}
      </div>
    </Router>
  );
}

export default App;