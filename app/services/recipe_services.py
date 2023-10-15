import re
from core.database import MongoDBConnector
from bson.objectid import ObjectId
from exceptions.recipe_exceptions import InvalidRecipeIDException, RecipeNotFoundException
from models.recipe import RecipeDatabaseIn, RecipeDatabaseUpdate

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

async def insert_recipe(recipe_database_in: RecipeDatabaseIn) -> str:
    try:
        result = await recipe_db_collection.insert_one(recipe_database_in)

        if result:
            return str(result.inserted_id)

        return None
    except Exception as e:
        raise e

async def update_one_recipe(recipe_database_update: RecipeDatabaseUpdate) -> bool:
    try:
        result = await recipe_db_collection.update_one(
                {"_id": ObjectId(recipe_database_update.recipe_id)},
                {
                    "$set": {
                        "recipe_name": recipe_database_update.recipe_name,
                        "recipe_description": recipe_database_update.recipe_description,
                        "ingredients": recipe_database_update.ingredients,
                        "steps": recipe_database_update.steps,
                        "total_time": recipe_database_update.total_time,
                        "difficulty": recipe_database_update.difficulty,
                        "servings": recipe_database_update.servings,
                        "image_files": recipe_database_update.image_files,
                        "last_updated_by": recipe_database_update.last_updated_by,
                        "last_updated_date": recipe_database_update.last_updated_date
                    }
                }
            )
        if result.modified_count == 1:
            return True
        else:
            return False
    except Exception as e:
        raise e
