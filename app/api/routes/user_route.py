
from fastapi import APIRouter, HTTPException, Body, Depends

from models.response import SuccessOut, ErrorOut
from models.user import UserRegisterModel, UserUpdatePasswordModel, UserUpdateDisplayNameModel

from utils.logger import logger

from services.auth_services import validate_token
from services.user_services import User
from exceptions.user_exceptions import UserNotFoundException, DisplayNameExistException, UserAlreadyExistsException, PasswordsDoNotMatchException, PasswordsMatchException, UserIdNotFoundException, InvalidPasswordException


router = APIRouter()
from utils.logger import logger


@router.get("/")
async def root():
    return {"route": "user"}


@router.post("/register")
async def register(user_register_model: UserRegisterModel  = Body(...)):
    try:
        user = User(user_register_model)

        await user.create_user()

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
async def get_user(user_id: str = Depends(validate_token)):
    try:
        user = User()

        user.set_id(user_id)

        payload = {
            "email": user.get_email(), 
            "display_name": user.get_display_name(), 
        }

        return SuccessOut(payload=payload)
    
    except UserNotFoundException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())
    

@router.post("/update_password")
async def update_password(user_update_password_model: UserUpdatePasswordModel  = Body(...), user_id: str = Depends(validate_token)):
    try:
        user = User(user_update_password_model)

        user.set_id(user_id)

        await user.get_user()

        await user.update_password()

        return SuccessOut(message="Password updated successfully")
    
    except PasswordsMatchException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except InvalidPasswordException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except UserIdNotFoundException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())
    

@router.post("/update_display_name")
async def update_display_name(user_update_display_name_model: UserUpdateDisplayNameModel  = Body(...), user_id: str = Depends(validate_token)):
    try:
        user = User()

        user.set_id(user_id)

        await user.get_user()

        user.set_display_name(user_update_display_name_model.new_display_name)
        print(user_update_display_name_model.new_display_name)
        await user.update_display_name()

        return SuccessOut(message="Display name updated successfully")

    except DisplayNameExistException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except InvalidPasswordException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except UserIdNotFoundException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())

