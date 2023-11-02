from core.database import MongoDBConnector
from bson.objectid import ObjectId
from exceptions.recipe_exceptions import InvalidRecipeIDException
from exceptions.review_exceptions import InvalidReviewIDException, ReviewNotFoundException
from models.review import ReviewDatabaseIn
 
# Get singleton db connection
review_db_collection = MongoDBConnector.get_client()["dishswapdb"]["reviews"]

async def get_reviews(page, recipe_id):
    try:
        if recipe_id and not ObjectId.is_valid(recipe_id):
            raise InvalidRecipeIDException(recipe_id)
        
        count = await get_reviews_count(recipe_id)
        pipeline = [
            {
                "$match": {"recipe_id": ObjectId(recipe_id)} if recipe_id else {}
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

async def get_reviews_user(page, user_id):
    try:
        count = await review_db_collection.count_documents({"created_by": ObjectId(user_id)})
        reviews = [review async for review in review_db_collection.find(
            {"created_by": ObjectId(user_id)}, 
            skip=9*(int(page)-1), 
            limit=9
        )]

        reviews = [review async for review in review_db_collection.aggregate([
            {
                "$match": {"created_by": ObjectId(user_id)} if user_id else {}
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
                "$project": 
                    {
                        "recipe":
                            {
                                "recipe_description": 0,
                                "ingredients": 0,
                                "steps": 0,
                                "total_time": 0,
                                "difficulty": 0,
                                "servings": 0,
                                "image_files": 0,
                                "created_by": 0,
                                "created_date": 0,
                                "last_updated_by": 0,
                                "last_updated_date": 0,
                            }
                    }
            }
        ])]

        return {"count": count, "reviews": reviews}
    except Exception as e:
        raise e

async def get_reviews_count(recipe_id):
    try:
        if recipe_id and not ObjectId.is_valid(recipe_id):
            raise InvalidRecipeIDException(recipe_id)
        
        count = await review_db_collection.count_documents({"recipe_id": ObjectId(recipe_id)} if recipe_id else {})
        
        return count
    except Exception as e:
        raise e

async def get_review(review_id):
    try:
        if not ObjectId.is_valid(review_id):
            raise InvalidReviewIDException(review_id)

        review = await review_db_collection.find_one({"_id": ObjectId(review_id)})

        if review is None:
            raise ReviewNotFoundException(review_id)
        
        return review
        
    except Exception as e:
        raise

async def check_review_exists(recipe_id, user_id):
    try:
        if not ObjectId.is_valid(recipe_id):
            raise InvalidRecipeIDException(recipe_id)

        review = await review_db_collection.find_one({"recipe_id": ObjectId(recipe_id), "created_by": ObjectId(user_id)})
        
        return bool(review)
        
    except Exception as e:
        raise

async def insert_review(review_database_in: ReviewDatabaseIn) -> str:
    try:
        result = await review_db_collection.insert_one(review_database_in)

        if result:
            return str(result.inserted_id)

        return None
    except Exception as e:
        raise e

async def delete_one_review(review_id: str) -> bool:
    try:
        if not ObjectId.is_valid(review_id):
            raise InvalidReviewIDException(review_id)
        
        result = await review_db_collection.delete_one({"_id": ObjectId(review_id)})
        
        if result.deleted_count == 1:
            return True
        else:
            return False

    except Exception as e:
        raise e 

async def delete_recipe_reviews(recipe_id: str) -> bool:
    try:
        if not ObjectId.is_valid(recipe_id):
            raise InvalidRecipeIDException(recipe_id)
        
        await review_db_collection.delete_many({"recipe_id": ObjectId(recipe_id)})
        
        return True

    except Exception as e:
        raise e 

