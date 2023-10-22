
from fastapi import APIRouter, HTTPException, Body, Request, Depends

from models.response import SuccessOut, ErrorOut
from models.user import UserRegister, UserDatabaseIn, UserChangePassword


from utils.hasher import hash_password
from utils.logger import logger

from utils.hasher import hash_password, validate_password


from services.user_services import create_user, check_passwords, check_user_exist, update_password_by_id, check_passwords_not_same, check_user_exist_with_id 
from services.auth_services import validate_token

from exceptions.user_exceptions import UserAlreadyExistsException, PasswordsDoNotMatchException, PasswordsMatchException, UserIdNotFoundException, PasswordDoesNotMatchDatabaseException


router = APIRouter()
from utils.logger import logger


@router.get("/")
async def root():
    return {"route": "user"}


@router.post("/register")
async def register(request: Request, user_register: UserRegister  = Body(...)):
    try:
        client_ip = request.client.host

        check_passwords(user_register.password, user_register.confirm_password)

        await check_user_exist(user_register.email, user_register.display_name)

        hashed_password = hash_password(user_register.password)

        user_database_in = UserDatabaseIn(email=user_register.email, display_name=user_register.display_name, hashed_password=hashed_password, user_type="user")

        await create_user(user_database_in)

        return SuccessOut(message="User registered successfully")
    
    except UserAlreadyExistsException as e:
        logger.info(f'IP: {client_ip} Message: {e}')
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except PasswordsDoNotMatchException as e:
        logger.info(f'IP: {client_ip} Message: {e}')
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:

        logger.error(f'IP: {client_ip} Message: {e}')
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())


@router.post("/update_password")
async def update_password(user_change_password: UserChangePassword  = Body(...), user_id: str = Depends(validate_token)):
    try:
        challenge_password = user_change_password.current_password
        new_password = user_change_password.new_password

        check_passwords_not_same(challenge_password, new_password)

        user_info = await check_user_exist_with_id(user_id)
            
        validate_password(challenge_password, user_info.hashed_password)
        
        new_hashed_password = hash_password(new_password)

        await update_password_by_id(user_id, new_hashed_password)

        return SuccessOut(message="Password updated successfully")
    
    except PasswordsMatchException as e:
        # Log e
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except PasswordDoesNotMatchDatabaseException as e:
        # Log e
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except UserIdNotFoundException as e:
        # Log e
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
