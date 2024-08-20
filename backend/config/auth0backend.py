import json
import requests
from jose import jwt, jwk
from django.conf import settings
from rest_framework import authentication, exceptions

class Auth0JSONWebTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return None

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            raise exceptions.AuthenticationFailed('Authorization header must start with Bearer')
        elif len(parts) == 1:
            raise exceptions.AuthenticationFailed('Token not found')
        elif len(parts) > 2:
            raise exceptions.AuthenticationFailed('Authorization header must be Bearer token')

        token = parts[1]
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:
            raise exceptions.AuthenticationFailed('Invalid header. Use an RS256 signed JWT Access Token')

        rsa_key = {}
        for key in settings.PUBLIC_KEY['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = jwk.construct(key)

        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key.to_pem().decode('utf-8'),
                    algorithms=['RS256'],
                    audience=settings.AUTH0_AUDIENCE,
                    issuer=settings.JWT_ISSUER
                )
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('Token is expired')
            except jwt.JWTClaimsError:
                raise exceptions.AuthenticationFailed('Incorrect claims, please check the audience and issuer')
            except Exception as e:
                raise exceptions.AuthenticationFailed(f'Unable to parse authentication token: {str(e)}')

            return (payload, token)
        raise exceptions.AuthenticationFailed('Unable to find appropriate key')