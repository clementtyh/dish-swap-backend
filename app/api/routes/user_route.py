from fastapi import APIRouter, HTTPException, Body

from models.response import SuccessOut, ErrorOut
from models.user import UserRegister, UserDatabaseIn

from utils.hasher import hash_password

from services.user_services import create_user, check_passwords, check_user_exist

from exceptions.user_exceptions import UserAlreadyExistsException, PasswordsDoNotMatchException, UserNotFoundException, LoginPasswordDoesNotMatchException


router = APIRouter()


@router.get("/")
async def root():
    return {"route": "user"}


@router.post("/register")
async def register(user_register: UserRegister  = Body(...)):
    try:
        check_passwords(user_register.password, user_register.confirm_password)

        await check_user_exist(user_register.email, user_register.display_name)

        hashed_password = hash_password(user_register.password)

        user_database_in = UserDatabaseIn(email=user_register.email, display_name=user_register.display_name, hashed_password=hashed_password, user_type="user")

        await create_user(user_database_in)

        return SuccessOut()
    
    except UserAlreadyExistsException as e:
        # Log e
        raise HTTPException(status_code=400, detail=str(e))
    except PasswordsDoNotMatchException as e:
        # Log e
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="An unknown error has occurred")
