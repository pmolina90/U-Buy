import axios from 'axios'; 

const getAccessToken = async () => {
   try { 
    const response = await axios.post(
       'https://dev-iq3rsvc4so7gvwzi.us.auth0.com/oauth/token',
       {
           grant_type: 'client_credentials',
           client_id: process.env.REACT_APP_AUTH0_CLIENT_ID,
           client_secret: process.env.REACT_APP_AUTH0_CLIENT_SECRET,
           audience: process.env.REACT_APP_AUTH0_AUDIENCE
       },
       {
           headers: {
            'content-type': 'application/json',
           }
        }
    );
    
    return response.data.access_token;
  } catch (error) {
    // Log detailed error information
    console.error("Error getting access token: ", error);
    if (error.response) {
        console.error("Status:", error.response.status);
        console.error("Data:", error.response.data);
    } else if (error.request) {
        console.error("Request:", error.request);
    } else {
        console.error("Error Message:", error.message);
    }
    throw error;
}
};

// Get user roles
const getUserRoles = async (userId) => {
  try {
    const accessToken = await getAccessToken();
    const response = await axios.get(
        `https://dev-iq3rsvc4so7gvwzi.us.auth0.com/api/v2/users/${userId}/roles`,
        {
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        }
    );

    return response.data;
 } catch (error) {
    console.error("Error getting user roles: ", error);
    throw error;
 }
};

export { getAccessToken, getUserRoles };