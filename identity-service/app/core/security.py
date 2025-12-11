import jwt
import uuid
import datetime

from .exceptions import JWTException

class JWTUtils:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def extract_token(self, authorization_header: str) -> str:
        """
        Extracts the token from the Authorization header.
        """
        try:
            scheme, token = authorization_header.split(" ")
            if scheme.lower() != "bearer":
                raise JWTException("Invalid authorization scheme")
            return token
        except ValueError:
            raise JWTException("Invalid authorization header format")

    def encode(self, user_id: uuid.UUID, email: str) -> str:
        """
        Encodes a payload into a JWT token.
        """
        payload = {
            "sub" : str(user_id),
            "email": email,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=3)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def decode(self, token: str) -> dict:
        """
        Decodes a JWT token into a payload.
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise JWTException("Token has expired")
        except jwt.InvalidTokenError:
            raise JWTException("Invalid token")