import os
import requests
from django.conf import settings

# Load environment variables
AUTH0_DOMAIN = settings.AUTH0_DOMAIN
AUTH0_CLIENT_ID = settings.AUTH0_M2M_CLIENT_ID
AUTH0_CLIENT_SECRET = settings.AUTH0_M2M_CLIENT_SECRET
AUTH0_AUDIENCE = settings.AUTH0_AUDIENCE

def get_auth0_access_token():
    url = f''
    headers = {'content-type': 'application/json'}
    payload = {
        'grant_type': 'client_credentials',
        'client_id': AUTH0_CLIENT_ID,
        'client_secret': AUTH0_CLIENT_SECRET,
        'audience': AUTH0_AUDIENCE
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json().get('access_token')

def get_user_roles(user_id):
    token = get_auth0_access_token()
    url = f''
    headers = {
        'Authorization': f'Bearer {token}',
        'content-type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Example usage in a view or service
def example_usage():
    user_id = 'auth0|some-user-id'
    roles = get_user_roles(user_id)
    print(f'Roles for user {user_id}: {roles}')