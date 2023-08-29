from bson.objectid import ObjectId

from models.user import UserDatabaseIn

from core.database import MongoDBConnector

from exceptions.user_exceptions import UserAlreadyExistsException, PasswordsDoNotMatchException

# Get singleton db connection
user_db_collection = MongoDBConnector.get_client()["dishswapdb"]["users"]


def check_passwords(password: str, confirm_password: str):
    if password != confirm_password: raise PasswordsDoNotMatchException


async def check_user_exist(email: str, display_name: str):
    try:
        query = {}

        if email:
            query["email"] = email
        if display_name:
            query["display_name"] = display_name

        document = await user_db_collection.find_one(query)

        if document is not None:
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
