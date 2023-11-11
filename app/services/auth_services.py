import os
import jwt
import bcrypt
import datetime
from fastapi import HTTPException,Request
from models.response import ErrorOut
from exceptions.user_exceptions import InvalidPasswordException
from utils.logger import logger


# Load your private and public keys
JWT_PUBLIC_KEY_PATH = os.getenv("JWT_PUBLIC_KEY_PATH")
JWT_PRIVATE_KEY_PATH = os.getenv("JWT_PRIVATE_KEY_PATH")


class AuthenticationServices():

    with open(JWT_PUBLIC_KEY_PATH, "r") as public_key_file:
        __public_key = public_key_file.read()

    with open(JWT_PRIVATE_KEY_PATH, "r") as private_key_file:
        __private_key = private_key_file.read()

    __algorithm = "RS256"


    def create_token(self, data: dict, minutes_to_expire: int):
        expiration =  datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes_to_expire)
        return jwt.encode({"exp": expiration, **data}, self.__private_key, algorithm=self.__algorithm)
    

    def verify_token(self, token: str):
        try:
            return jwt.decode(token, self.__public_key, algorithms=[self.__algorithm])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail=ErrorOut(message="Token has expired").model_dump())
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail=ErrorOut(message="Invalid token").model_dump())
        except Exception as e:
            raise

    
    def validate_token(self, request: Request) -> str:
        try:
            # Extract the token from the Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail=ErrorOut(message="Invalid authorization header").model_dump())
            token = auth_header.split("Bearer ")[1]
            
            # Verify the token
            payload = self.verify_token(token)
            
            return payload['id']
        
        except Exception as e:
            raise


    def validate_password(self, challenge_password: str, hashed_password: str):
        try:
            challenge_password = challenge_password.encode("utf-8")
            hashed_password = hashed_password.encode("utf-8")
            if not bcrypt.checkpw(challenge_password, hashed_password):
                raise InvalidPasswordException

        except Exception as e:
            logger.error(e)
            raise

    
    def validate_token_unhandled(self, request: Request) -> str:
        try:
            # Extract the token from the Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail=ErrorOut(message="Invalid authorization header").model_dump())
            token = auth_header.split("Bearer ")[1]
            
            # Verify the token
            payload = self.verify_token(token)
            
            return payload['id']
        
        except Exception as e:
            return ""