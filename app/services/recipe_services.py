import re
from core.database import MongoDBConnector
from bson.objectid import ObjectId
from exceptions.recipe_exceptions import InvalidRecipeIDException, RecipeNotFoundException, RecipeAlreadyExistsException
from models.recipe import RecipeDatabaseIn

# Get singleton db connection
recipe_db_collection = MongoDBConnector.get_client()["dishswapdb"]["recipes"]

async def get_recipes(page, search):
    try:
        search_regx = re.compile(fr'.*{re.escape(search)}.*', re.IGNORECASE)

        count = await recipe_db_collection.count_documents(
            {'$or': [{'recipe_name': {'$regex': search_regx}}, 
                    {'recipe_description': {'$regex': search_regx}}]}
        )
        recipes = [recipe async for recipe in recipe_db_collection.find(
            {'$or': [{'recipe_name': {'$regex': search_regx}}, 
                    {'recipe_description': {'$regex': search_regx}}]}, 
            skip=9*(int(page)-1), 
            limit=9
        )]

        return {"count": count, "recipes": recipes}
        
    except Exception as e:
        raise

async def get_recipe(id):
    try:
        if not ObjectId.is_valid(id):
            raise InvalidRecipeIDException(id)

        recipe = await recipe_db_collection.find_one({"_id": ObjectId(id)})

        if recipe is None:
            raise RecipeNotFoundException(id)
        
        return recipe
        
    except Exception as e:
        raise

async def check_recipe_exist(recipe_name):
    try:
        existing_recipe = await recipe_db_collection.find_one({"recipe_name": recipe_name})
        if existing_recipe is not None:
            raise RecipeAlreadyExistsException(recipe_name)

    except Exception as e:
        raise e

async def create_recipe(recipe_database_in: RecipeDatabaseIn) -> bool:
    try:
        result = await recipe_db_collection.insert_one(recipe_database_in)
        
        if result:
            return True

        return False
    
    except Exception as e:
        raise e