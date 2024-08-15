import axios from 'axios';
import axiosInstance from './axiosInstance'; // Import axiosInstance to set default headers

export const login = async (username, password) => {
    try {
        const response = await axios.post('/api/v1/login/', { 
            username, 
            password, 
        });
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        axiosInstance.defaults.headers['Authorization'] = `Bearer ${response.data.access}`;
        return response.data;
    } catch (error) {
        console.error('Error logging in', error);
        throw error;
    }
};

export const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    delete axiosInstance.defaults.headers['Authorization'];
};