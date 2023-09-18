import os
import jwt
import datetime
from fastapi import HTTPException,Request
from models.response import ErrorOut


# Load your private and public keys
JWT_PUBLIC_KEY_PATH = os.getenv("JWT_PUBLIC_KEY_PATH")
JWT_PRIVATE_KEY_PATH = os.getenv("JWT_PRIVATE_KEY_PATH")

with open(JWT_PUBLIC_KEY_PATH, "r") as public_key_file:
    PUBLIC_KEY = public_key_file.read()

with open(JWT_PRIVATE_KEY_PATH, "r") as private_key_file:
    PRIVATE_KEY = private_key_file.read()


ALGORITHM = "RS256"


def create_token(data: dict):
    expiration =  datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    return jwt.encode({"exp": expiration, **data}, PRIVATE_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        return jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail=ErrorOut(message="Token has expired").model_dump())
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail=ErrorOut(message="Invalid token").model_dump())
    except Exception as e:
        raise


def validate_token(request: Request) -> str:
    try:
        # Extract the token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail=ErrorOut(message="Invalid authorization header").model_dump())
        token = auth_header.split("Bearer ")[1]
        
        # Verify the token
        payload = verify_token(token)
        
        return payload['id']
    
    except Exception as e:
        raise