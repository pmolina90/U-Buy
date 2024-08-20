import React from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';

function LoginComponent({ onLoginSuccess }) {
    const { loginWithRedirect, getIdTokenClaims } = useAuth0();
    const navigate = useNavigate();

    const handleLogin = async () => {
        await loginWithRedirect();
        
        // After successful login, get the ID token
        const idToken = await getIdTokenClaims();
        const token = idToken.__raw;

        try {
            // Send the ID token to your Django backend
            const response = await axios.post('api/token', { token });

            // Extract and store the JWT tokens from your backend response
            const { access, refresh } = response.data;
            localStorage.setItem('access_token', access);
            localStorage.setItem('refresh_token', refresh);

            onLoginSuccess();
            navigate('/store');
        } catch (error) {
            console.error('Error logging in:', error);
        }
    };

    return (
        <div>
            <h1>Login</h1>
            <button onClick={handleLogin}>Login with Auth0</button>
        </div>
    );
}

export default LoginComponent;