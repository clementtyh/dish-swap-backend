import re
from core.database import MongoDBConnector
from bson.objectid import ObjectId
from exceptions.recipe_exceptions import InvalidRecipeIDException, RecipeNotFoundException
from exceptions.user_exceptions import InvalidUserIDException
from models.recipe import RecipeDatabaseIn, RecipeDatabaseUpdate
from services.flavourmark_services import get_flavourmark, get_flavourmarks_count

# Get singleton db connection
recipe_db_collection = MongoDBConnector.get_client()["dishswapdb"]["recipes"]
flavourmark_db_collection = MongoDBConnector.get_client()["dishswapdb"]["flavourmarks"]

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

async def get_recipes_user(page, user_id):
    try:
        count = await recipe_db_collection.count_documents({"created_by": ObjectId(user_id)})
        recipes = [recipe async for recipe in recipe_db_collection.find(
            {"created_by": ObjectId(user_id)}, 
            skip=9*(int(page)-1), 
            limit=9
        )]

        return {"count": count, "recipes": recipes}
        
    except Exception as e:
        raise

async def get_flavourmarked_recipes(page, user_id):
    try:
        count = await flavourmark_db_collection.count_documents({"user_id": ObjectId(user_id)})
        recipes = [doc["recipe"] async for doc in flavourmark_db_collection.aggregate([
            {
                "$skip": 9*(int(page)-1)
            },
            {
                "$limit": 9
            },
            {
                "$match": {
                    "user_id": ObjectId(user_id)
                }
            },
            {
                "$lookup": {
                    "from": "recipes",
                    "localField": "recipe_id",
                    "foreignField": "_id",
                    "as": "recipe"
                }
            },
            {
                "$unwind": "$recipe"
            },
            {
                "$project": {
                    "recipe": 1,
                    "_id": 0,
                }
            }
        ])]

        return {"count": count, "recipes": recipes}
        
    except Exception as e:
        raise

async def get_recipe(recipe_id, user_id):
    try:
        if not ObjectId.is_valid(recipe_id):
            raise InvalidRecipeIDException(recipe_id)
        
        recipe = await recipe_db_collection.find_one({"_id": ObjectId(recipe_id)})

        if recipe is None:
            raise RecipeNotFoundException(recipe_id)
        
        flavourmarks_count = await get_flavourmarks_count(recipe_id)
                
        is_flavourmarked = False
        if user_id:
            flavourmark = await get_flavourmark(recipe_id, user_id)
            is_flavourmarked = bool(flavourmark)

        recipe["flavourmarks_count"] = flavourmarks_count
        recipe["is_flavourmarked"] = is_flavourmarked
        
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
    
async def toggle_recipe_flavourmark(recipe_id, user_id):
    try:
        if not ObjectId.is_valid(recipe_id):
            raise InvalidRecipeIDException(recipe_id)
        
        if not ObjectId.is_valid(user_id):
            raise InvalidUserIDException(user_id)
        
        recipe = await recipe_db_collection.find_one({"_id": ObjectId(recipe_id)})
        if recipe is None:
            raise InvalidRecipeIDException(recipe_id)
        
        flavourmark = await get_flavourmark(recipe_id, user_id)

        if (flavourmark):
            result = await flavourmark_db_collection.delete_one({"_id": flavourmark["_id"]})
            if result.deleted_count == 1:
                return True
            else:
                return False
        else:
            result = await flavourmark_db_collection.insert_one(
                {
                    "recipe_id": ObjectId(recipe_id),
                    "user_id": ObjectId(user_id)
                },
            )
            if result:
                return True
            else:
                return False

    except Exception as e:
        raise e

async def delete_one_recipe(recipe_id: str) -> bool:
    try:
        if not ObjectId.is_valid(recipe_id):
            raise InvalidRecipeIDException(recipe_id)

        result = await recipe_db_collection.delete_one({"_id": ObjectId(recipe_id)})

        if result.deleted_count == 1:
            return True
        else:
            return False
    except Exception as e:
        raise e
