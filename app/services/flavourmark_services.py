from core.database import MongoDBConnector
from bson.objectid import ObjectId
from exceptions.recipe_exceptions import InvalidRecipeIDException

flavourmark_db_collection = MongoDBConnector.get_client()["dishswapdb"]["flavourmarks"]


async def get_flavourmarks_count(recipe_id):
    try:
        if recipe_id and not ObjectId.is_valid(recipe_id):
            raise InvalidRecipeIDException(recipe_id)
        
        count = await flavourmark_db_collection.count_documents({"recipe_id": ObjectId(recipe_id)} if recipe_id else {})
        
        return count
    except Exception as e:
        raise e

async def delete_recipe_flavourmarks(recipe_id: str) -> bool:
    try:
        if not ObjectId.is_valid(recipe_id):
            raise InvalidRecipeIDException(recipe_id)
        
        await flavourmark_db_collection.delete_many({"recipe_id": ObjectId(recipe_id)})
        
        return True

    except Exception as e:
        raise e 