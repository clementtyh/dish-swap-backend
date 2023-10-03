from core.database import MongoDBConnector
from bson.objectid import ObjectId
from exceptions.recipe_exceptions import InvalidRecipeIDException, RecipeNotFoundException, RecipeAlreadyExistsException, InvalidRecipeOperationException
from models.recipe import RecipeDatabaseIn

# Get singleton db connection
recipe_db_collection = MongoDBConnector.get_client()["dishswapdb"]["recipes"]

async def get_recipes(page, user_id):
    try:
        count = await recipe_db_collection.count_documents({})
        recipes = [recipe async for recipe in recipe_db_collection.find({}, {
            "name": 1,
            "imgPath": 1,
            "description": 1,
            "display_name": 1,
            "ingredients": 1,
            "preparationSteps": 1,
            "nutrition": 1,
            "difficulty": 1,
            "totalTime": 1,
            "servings": 1,
            "reviews": 1,
            "flavourmarkCount": 1,
            "flavourmarks": { 
                "$elemMatch": { "$eq": ObjectId(user_id) }
            } if user_id else 1
        }, skip=9*(int(page)-1), limit=9)]

        return {"count": count, "recipes": recipes}
        
    except Exception as e:
        raise

async def get_recipe(id, user_id):
    try:
        if not ObjectId.is_valid(id):
            raise InvalidRecipeIDException(id)

        recipe = await recipe_db_collection.find_one({"_id": ObjectId(id)}, {
            "name": 1,
            "imgPath": 1,
            "description": 1,
            "display_name": 1,
            "ingredients": 1,
            "preparationSteps": 1,
            "nutrition": 1,
            "difficulty": 1,
            "totalTime": 1,
            "servings": 1,
            "reviews": 1,
            "flavourmarkCount": 1,
            "flavourmarks": { 
                "$elemMatch": { "$eq": ObjectId(user_id) }
            } if user_id else 1
        })

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
    
async def add_flavourmark_recipe(id, user_id):
    try:
        if not ObjectId.is_valid(id):
            raise InvalidRecipeIDException(id)

        result = await recipe_db_collection.update_one(
            { 
                "_id": ObjectId(id), 
                "flavourmarks": { "$ne": ObjectId(user_id) }
            },
            {
                "$inc": { "flavourmarkCount": 1 },
                "$push": { "flavourmarks": ObjectId(user_id) }
            }
        )

        if not result.modified_count:
            raise InvalidRecipeOperationException(id)
        
        return True
                
    except Exception as e:
        raise

async def remove_flavourmark_recipe(id, user_id):
    try:
        if not ObjectId.is_valid(id):
            raise InvalidRecipeIDException(id)

        result = await recipe_db_collection.update_one(
            { 
                "_id": ObjectId(id), 
                "flavourmarks": ObjectId(user_id)
            },
            {
                "$inc": { "flavourmarkCount": -1 },
                "$pull": { "flavourmarks": ObjectId(user_id) }
            }
        )

        if not result.modified_count:
            raise InvalidRecipeOperationException(id)
        
        return True
        
    except Exception as e:
        raise