import axios from 'axios';
import { getAccessToken } from './auth0-utils';// Import getAcessTokenSilently from auth0-utils.js, to verify the user's access token

const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/',
    headers: {
        'Content-Type': 'application/json',
    },
});

// add a request interceptor to attach the access token to every reques
axiosInstance.interceptors.request.use(
    async (config) => {
        try {
            // Retrieve the access token
            const accessToken = await getAccessToken();
            
            // Log the access token to verify it's being retrieved
            console.log('Access Token:', accessToken);
    
            // If the access token exists, set it in the Authorization header
            if (accessToken) {
                config.headers.Authorization = `Bearer ${accessToken}`;
            }
        } catch (error) {
            console.error('Error retrieving access token', error);
        }
    
        return config;
    }, (error) => {
        // Do something with request error
        return Promise.reject(error);
    });

axiosInstance.interceptors.response.use(
    (response) => {
        return response;
    },
    async (error) => {
        const originalRequest = error.config;

        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            const refreshToken = localStorage.getItem('refresh_token');
            if (refreshToken) {
                try {
                    const response = await axios.post('http://127.0.0.1:8000/api/v1/token/refresh/', {
                        refresh: refreshToken,
                    });
                    localStorage.setItem('access_token', response.data.access);
                    axiosInstance.defaults.headers['Authorization'] = `Bearer ${response.data.access}`;
                    originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`;
                    return axiosInstance(originalRequest);
                } catch (error) {
                    console.error('Error refreshing token', error);
                }
            }
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;
