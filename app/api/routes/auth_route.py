from fastapi import APIRouter, Depends, HTTPException, Body, Request

from models.auth import Login
from models.response import SuccessOut, ErrorOut

from utils.logger import logger

from services.user_services import User
from services.auth_services import AuthenticationServices

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
        user = User()
        user.set_email(challenge_email)
        await user.get_user_by_email()

        authentication_services = AuthenticationServices()

        authentication_services.validate_password(challenge_password, user.get_hashed_password())

        minutes_to_expire = 60

        token = authentication_services.create_token({"id": user.get_id()}, minutes_to_expire)

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
async def verify(user_id: str = Depends(AuthenticationServices().validate_token)):
    try:
        return SuccessOut(message="Token is valid")
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())
