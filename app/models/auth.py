from fastapi import HTTPException
from pydantic import BaseModel, validator
from utils.validator import validate_jwt_token, validate_email, validate_alphanumeric_symbols
from models.response import ErrorOut


class Token(BaseModel):
    access_token: str

    @validator("access_token")
    def validate_model_email(cls, value):
        if not validate_jwt_token(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid token").model_dump())
        return value


class Login(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_model_email(cls, value):
        if not validate_email(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid email").model_dump())
        return value

    @validator("password")
    def validate_model_password(cls, value):
        # Do not use validate_password
        if not validate_alphanumeric_symbols(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid password").model_dump())
        return value