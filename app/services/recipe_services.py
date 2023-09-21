from core.database import MongoDBConnector
from bson.objectid import ObjectId
from exceptions.recipe_exceptions import InvalidRecipeIDException, RecipeNotFoundException

# Get singleton db connection
recipe_db_collection = MongoDBConnector.get_client()["dishswapdb"]["recipes"]

async def get_recipes(page):
    try:
        recipes = [recipe async for recipe in recipe_db_collection.find({}, skip=9*(int(page)-1), limit=9)]

        for recipe in recipes:
            recipe["_id"] = str(recipe["_id"])

        return recipes
        
    except Exception as e:
        raise

async def get_recipe(id):
    try:
        if not ObjectId.is_valid(id):
            raise InvalidRecipeIDException(id)

        recipe = await recipe_db_collection.find_one({"_id": ObjectId(id)})

        if recipe is None:
            raise RecipeNotFoundException(id)
        
        recipe["_id"] = str(recipe["_id"])

        return recipe
        
    except Exception as e:
        raise