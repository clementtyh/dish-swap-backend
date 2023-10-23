from fastapi import APIRouter, Depends, HTTPException, Body, Request

from models.auth import Login
from models.response import SuccessOut, ErrorOut

from utils.hasher import validate_password
from utils.logger import logger

from services.user_services import get_user_database_out
from services.auth_services import create_token, validate_token

from exceptions.user_exceptions import UserNotFoundException, InvalidPasswordException


router = APIRouter()


@router.get("/")
async def root():
    return {"route": "auth"}


@router.post("/login")
async def login(login: Login  = Body(...)):
    challenge_email = login.email
    challenge_password = login.password

    try:
        user_info = await get_user_database_out(challenge_email)

        validate_password(challenge_password, user_info.hashed_password)

        minutes_to_expire = 60

        token = create_token({"id": user_info.id}, minutes_to_expire)

        payload = {
            "token": token, 
        }

        response = SuccessOut(message="Login successful", payload=payload)

        return response

    except UserNotFoundException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except InvalidPasswordException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())


@router.post("/verify")
async def verify(user_id: str = Depends(validate_token)):
    try:
        return SuccessOut(message="Token is valid")
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())
