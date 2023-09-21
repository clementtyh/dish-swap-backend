from core.database import MongoDBConnector

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
