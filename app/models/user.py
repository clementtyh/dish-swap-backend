from pydantic import BaseModel, validator, Field
from fastapi import HTTPException
from utils.validator import validate_email, validate_display_name, validate_password



class UserRegister(BaseModel):
    email: str
    display_name: str
    password: str
    confirm_password: str

    @validator("email")
    def validate_email(cls, value):
        if not validate_email(value):
            raise HTTPException(status_code=400, detail="Email format is not valid")
        return value

    @validator("display_name")
    def validate_display_name(cls, value):
        if not validate_display_name(value):
            raise HTTPException(status_code=400, detail="Display name format is not valid")
        return value
    
    @validator("password")
    def validate_password(cls, value):
        if not validate_password(value):
            raise HTTPException(status_code=400, detail="Password does not meet the complexity requirements")
        return value

    @validator("confirm_password")
    def validate_confirm_password(cls, value):
        if not validate_password(value):
            raise HTTPException(status_code=400, detail="Password does not meet the complexity requirements")
        return value
    

class UserDatabaseIn(BaseModel):
    email: str
    display_name: str
    hashed_password: str
    user_type: str

    @validator("email")
    def validate_email(cls, value):
        if not validate_email(value):
            raise HTTPException(status_code=400, detail="Email format is not valid")
        return value

    @validator("display_name")
    def validate_display_name(cls, value):
        if not validate_display_name(value):
            raise HTTPException(status_code=400, detail="Display name format is not valid")
        return value
    

class UserDatabaseOut(BaseModel):
    id: str = Field(alias="_id")
    hashed_password: str
    user_type: str