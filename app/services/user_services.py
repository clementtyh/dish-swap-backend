from bson.objectid import ObjectId

from models.user import UserDatabaseIn

from core.database import MongoDBConnector

from exceptions.user_exceptions import UserAlreadyExistsException, PasswordsDoNotMatchException, UserNotFoundException
from models.user import UserDatabaseOut, UserProfile


# Get singleton db connection
user_db_collection = MongoDBConnector.get_client()["dishswapdb"]["users"]


def check_passwords(password: str, confirm_password: str):
    if password != confirm_password: raise PasswordsDoNotMatchException


async def check_user_exist(email: str, display_name: str):
    try:
        query = {}

        if email:
            query["$or"] = [{"email": email}]
        if display_name:
            query["$or"].append({"display_name": display_name})

        user_doc = await user_db_collection.find_one(query)

        if user_doc is not None:
            raise UserAlreadyExistsException
        
    except Exception as e:
        raise


async def create_user(user_database_in: UserDatabaseIn) -> bool:
    try:
        result = await user_db_collection.insert_one(user_database_in.model_dump())

        if result:
            return True

        return False
    except Exception as e:
        raise


async def get_user_database_out(email: str):
    try:
        user = await user_db_collection.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])

            return UserDatabaseOut(**user)

        raise UserNotFoundException(email)
    
    except Exception as e:
        raise


async def get_user_profile(email: str):
    try:
        user = await user_db_collection.find_one({"email": email})

        if user:
            return UserProfile(**user)

        raise UserNotFoundException(email)
    
    except Exception as e:
        raise


async def get_user_profile_with_id(id: str):
    try:
        user = await user_db_collection.find_one({"_id": ObjectId(id)})
        if user:
            user["_id"] = str(user["_id"])

            return UserProfile(**user)

        raise UserNotFoundException(id)
    
    except Exception as e:
        raise
