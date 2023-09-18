from fastapi import HTTPException
from pydantic import BaseModel, validator
from utils.validator import validate_jwt_token, validate_email, validate_alphanumeric_symbols
from models.response import ErrorOut


class Token(BaseModel):
    access_token: str

    @validator("access_token")
    def validate_email(cls, value):
        if not validate_jwt_token(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid token").model_dump())
        return value


class UserLogin(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, value):
        if not validate_email(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid email").model_dump())
        return value

    @validator("password")
    def validate_password(cls, value):
        if not validate_alphanumeric_symbols(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid password").model_dump())
        return value
    