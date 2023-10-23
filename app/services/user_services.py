from bson.objectid import ObjectId

from models.user import UserDatabaseIn

from core.database import MongoDBConnector

from exceptions.user_exceptions import UserAlreadyExistsException, PasswordsDoNotMatchException, UserNotFoundException, PasswordsMatchException, UserIdNotFoundException
from models.user import User, UserDatabaseOut, UserInfo


# Get singleton db connection
user_db_collection = MongoDBConnector.get_client()["dishswapdb"]["users"]


def check_passwords(password: str, confirm_password: str):
    if password != confirm_password: raise PasswordsDoNotMatchException


def check_passwords_not_same(current_password: str, new_password: str):
    if current_password == new_password: raise PasswordsMatchException


async def create_user(user_database_in: UserDatabaseIn) -> bool:
    try:
        result = await user_db_collection.insert_one(user_database_in.model_dump())

        if result:
            return True

        return False
    except Exception as e:
        raise


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


async def get_user_database_out_with_id(id: str):
    try:
        user = await user_db_collection.find_one({"_id": ObjectId(id)})
        if user:
            user["_id"] = str(user["_id"])

            return UserDatabaseOut(**user)

        raise UserIdNotFoundException(id)
    
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


async def get_user_info(email: str):
    try:
        user = await user_db_collection.find_one({"email": email})

        if user:
            return UserInfo(**user)

        raise UserNotFoundException(email)
    
    except Exception as e:
        raise


async def get_user(id: str):
    try:
        user = await user_db_collection.find_one({"_id": ObjectId(id)})
        if user:
            user["_id"] = str(user["_id"])

            return User(**user)

        raise UserIdNotFoundException(id)
    
    except Exception as e:
        raise


async def get_user_info_with_id(id: str):
    try:
        user = await user_db_collection.find_one({"_id": ObjectId(id)})
        if user:
            user["_id"] = str(user["_id"])

            return UserInfo(**user)

        raise UserIdNotFoundException(id)
    
    except Exception as e:
        raise


async def update_password_by_id(id, new_hashed_password):
    try:
        # Ensure the id is of type ObjectId
        if not isinstance(id, ObjectId):
            id = ObjectId(id)

        # Update the hashed password based on the _id
        result = await user_db_collection.update_one(
            {"_id": id},
            {"$set": {"hashed_password": new_hashed_password}}
        )
        
        # Check if the update was successful
        if result.modified_count > 0:
            return True
        else:
            raise UserIdNotFoundException(id)
            
    except Exception as e:
        raise


async def update_display_name_by_id(id, new_display_name):
    try:
        # Ensure the id is of type ObjectId
        if not isinstance(id, ObjectId):
            id = ObjectId(id)

        # Update the display_name based on the _id
        result = await user_db_collection.update_one(
            {"_id": id},
            {"$set": {"display_name": new_display_name}}
        )
        
        # Check if the update was successful
        if result.modified_count > 0:
            return True
        else:
            raise UserIdNotFoundException(id)
            
    except Exception as e:
        raise
