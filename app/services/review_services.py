from core.database import MongoDBConnector
from bson.objectid import ObjectId
from exceptions.recipe_exceptions import InvalidRecipeIDException

# Get singleton db connection
review_db_collection = MongoDBConnector.get_client()["dishswapdb"]["reviews"]

async def get_reviews(page, recipe):
    try:
        if recipe and not ObjectId.is_valid(recipe):
            raise InvalidRecipeIDException(recipe)
        
        count = await review_db_collection.count_documents({"recipe_id": ObjectId(recipe)} if recipe else {})
        pipeline = [
            {
                "$match": {"recipe_id": ObjectId(recipe)} if recipe else {}
            },
            {
                "$skip": 6*(int(page)-1)
            },
            {
                "$limit": 6
            },
            {
                "$lookup": 
                    {
                        "from": "users",
                        "localField": "created_by",
                        "foreignField": "_id",
                        "as": "created_by"
                    }
            },
            {
                "$unwind": "$created_by"
            },
            {
                "$project": 
                    {
                        "created_by":
                            {
                                "email": 0,
                                "hashed_password": 0,
                                "user_type": 0,
                            }
                    }
            }
        ]
        reviews = await review_db_collection.aggregate(pipeline).to_list(None)

        return {"count": count, "reviews": reviews}
        
    except Exception as e:
        raise

async def delete_recipe_reviews(recipe_id: str) -> bool:
    try:
        if not ObjectId.is_valid(recipe_id):
            raise InvalidRecipeIDException(recipe_id)
        
        await review_db_collection.delete_many({"recipe_id": ObjectId(recipe_id)})
        
        return True

    except Exception as e:
        raise e 