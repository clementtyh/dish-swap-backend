from bson.objectid import ObjectId

from models.user import UserDatabaseIn

from core.database import MongoDBConnector

from exceptions.user_exceptions import UserAlreadyExistsException, PasswordsDoNotMatchException

# Get singleton db connection
recipe_db_collection = MongoDBConnector.get_client()["dishswapdb"]["recipes"]


async def get_recipes():
    try:
        recipes = [recipe async for recipe in recipe_db_collection.find({}, skip=0, limit=1)]
        print(recipes)
        return recipes
        
    except Exception as e:
        raise
