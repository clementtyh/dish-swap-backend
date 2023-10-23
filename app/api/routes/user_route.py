
from fastapi import APIRouter, HTTPException, Body, Request, Depends

from models.response import SuccessOut, ErrorOut
from models.user import UserRegister, UserDatabaseIn, UserUpdatePassword


from utils.hasher import hash_password
from utils.logger import logger

from utils.hasher import hash_password, validate_password


from services.user_services import get_user, create_user, check_passwords, check_user_exist, update_password_by_id, check_passwords_not_same, get_user_database_out_with_id 
from services.auth_services import validate_token

from exceptions.user_exceptions import UserAlreadyExistsException, PasswordsDoNotMatchException, PasswordsMatchException, UserIdNotFoundException, PasswordDoesNotMatchDatabaseException


router = APIRouter()
from utils.logger import logger


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

        return SuccessOut(message="User registered successfully")
    
    except UserAlreadyExistsException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except PasswordsDoNotMatchException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())


@router.get("/get_user")
async def update_password(user_id: str = Depends(validate_token)):
    try:
        user = await get_user(user_id)

        payload = {
            "email": user.email, 
            "display_name": user.display_name, 
        }

        return SuccessOut(payload=payload)
    
    except UserIdNotFoundException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())
    

@router.post("/update_password")
async def update_password(user_update_password: UserUpdatePassword  = Body(...), user_id: str = Depends(validate_token)):
    try:
        challenge_password = user_update_password.current_password
        new_password = user_update_password.new_password

        check_passwords_not_same(challenge_password, new_password)

        user_info = await get_user_database_out_with_id(user_id)
            
        validate_password(challenge_password, user_info.hashed_password)
        
        new_hashed_password = hash_password(new_password)

        await update_password_by_id(user_id, new_hashed_password)

        return SuccessOut(message="Password updated successfully")
    
    except PasswordsMatchException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except PasswordDoesNotMatchDatabaseException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except UserIdNotFoundException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())


@router.post("/update_display_name")
async def update_display_name(user_update_password: UserUpdatePassword  = Body(...), user_id: str = Depends(validate_token)):
    pass