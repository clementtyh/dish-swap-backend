from pydantic import BaseModel, validator, Field
from fastapi import HTTPException
from utils.validator import validate_email, validate_display_name, validate_password
from models.response import ErrorOut


class UserRegister(BaseModel):
    email: str
    display_name: str
    password: str
    confirm_password: str

    @validator("email")
    def validate_model_email(cls, value):
        if not validate_email(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid email").model_dump())
        return value

    @validator("display_name")
    def validate_model_display_name(cls, value):
        if not validate_display_name(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid display name").model_dump())
        return value
    
    @validator("password")
    def validate_model_password(cls, value):
        if not validate_password(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Password does not meet the complexity requirements").model_dump())
        return value

    @validator("confirm_password")
    def validate_model_confirm_password(cls, value):
        if not validate_password(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Password does not meet the complexity requirements").model_dump())
        return value
    

class UserDatabaseIn(BaseModel):
    email: str
    display_name: str
    hashed_password: str
    user_type: str

    @validator("email")
    def validate_model_email(cls, value):
        if not validate_email(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid email").model_dump())
        return value

    @validator("display_name")
    def validate_model_display_name(cls, value):
        if not validate_display_name(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid display name").model_dump())
        return value
    

class UserDatabaseOut(BaseModel):
    id: str = Field(alias="_id")
    hashed_password: str
    user_type: str
    display_name: str


    
class UserProfile(BaseModel):
    email: str
    display_name: str
    user_type: str

    @validator("email")
    def validate_model_email(cls, value):
        if not validate_email(value):
            raise HTTPException(status_code=400, detail="Invalid email")
        return value

    @validator("display_name")
    def validate_model_display_name(cls, value):
        if not validate_display_name(value):
            raise HTTPException(status_code=400, detail="Invalid display name")
        return value


class UserChangePassword(BaseModel):
    current_password: str
    new_password: str

    @validator("current_password")
    def validate_current_password(cls, value):
        if not validate_password(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Current password does not meet the complexity requirements").model_dump())
        return value

    @validator("new_password")
    def validate_new_password(cls, value):
        if not validate_password(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="New password does not meet the complexity requirements").model_dump())
        return value
    