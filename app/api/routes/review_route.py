from fastapi import APIRouter, HTTPException, Body, Response, Depends
from typing import List
from services.review_services import *
from services.auth_services import validate_token
from models.response import ErrorOut, SuccessOut
from models.review import *
from utils.logger import logger
from services.recipe_services import get_recipe
from exceptions.recipe_exceptions import RecipeNotFoundException
from exceptions.review_exceptions import *

router = APIRouter()


@router.get("/", response_model=List[ReviewDatabaseOut])
async def root(response: Response, page=1, recipe=""):
    try:
        result = await get_reviews(page, recipe)
        response.headers["X-Total-Count"] = str(result["count"])

        return result["reviews"]

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())
    
@router.get("/profile", response_model=List[ProfileReviewDatabaseOut])
async def get_user_reviews(response: Response, page=1, user_id: str = Depends(validate_token)):
    try:
        result = await get_reviews_user(page, user_id)
        response.headers["X-Total-Count"] = str(result["count"])

        return result["reviews"]

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())
    
@router.post("/create")
async def create_review(review_data: Review = Body(...), user_id: str = Depends(validate_token)
):
    try:
        recipe_exist = await get_recipe(review_data.recipe_id, user_id)
        
        if recipe_exist:
            review_database_in = ReviewDatabaseIn(
            text = review_data.text,
            rating = review_data.rating,
            recipe_id = PydanticObjectId(recipe_exist["_id"]),
            created_by=PydanticObjectId(user_id),
            created_date= datetime.now(),
            last_updated_by=PydanticObjectId(user_id),
            last_updated_date=datetime.now())

            review_id = await insert_review(review_database_in.model_dump())
            if (review_id is not None):
                return SuccessOut(message="Review created successfully")
            else:
                return ErrorOut(message="Failed to create the review")
            
    except RecipeNotFoundException as e:
        logger.info(e)
        raise HTTPException(status_code=404, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=ErrorOut(message=str(e)).model_dump())
    
@router.post("/delete/{review_id}", response_model=SuccessOut)
async def delete_review(review_id: str, user_id: str = Depends(validate_token)
):
    try:
        existing_review = await get_review(review_id)

        if user_id != str(existing_review['created_by']):
            raise UnauthorisedReviewModificationException(review_id)

        delete_review_success = await delete_one_review(review_id)

        if delete_review_success:
            return SuccessOut(message="Review deleted successfully")
        else:
            return ErrorOut(message="Failed to delete the review")
        
    except InvalidReviewIDException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except ReviewNotFoundException as e:
        logger.info(e)
        raise HTTPException(status_code=404, detail=ErrorOut(message=str(e)).model_dump())
    except UnauthorisedReviewModificationException as e:
        logger.info(e)
        raise HTTPException(status_code=403, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())