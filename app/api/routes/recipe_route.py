from fastapi import APIRouter, HTTPException, Body, Response, Depends, Request
from typing import List
from services.auth_services import validate_token, validate_token_unhandled
from utils.logger import logger
from services.recipe_services import *
from services.review_services import delete_recipe_reviews, get_reviews_count
from services.flavourmark_services import delete_recipe_flavourmarks, get_flavourmarks_count
from models.response import ErrorOut, SuccessOut
from models.recipe import *
from exceptions.recipe_exceptions import *
from datetime import datetime
from api.routes.file_route import delete_cloudinary_images


router = APIRouter()


@router.get("/", response_model=List[RecipeDatabaseOut])
async def root(response: Response, page=1, search=""):
    try:
        result = await get_recipes(page, search)
        response.headers["X-Total-Count"] = str(result["count"])

        return result["recipes"]

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    
@router.get("/profile", response_model=List[RecipeDatabaseOut])
async def get_user_recipes(response: Response, page=1, user_id: str = Depends(validate_token)):
    try:
        result = await get_recipes_user(page, user_id)
        response.headers["X-Total-Count"] = str(result["count"])

        return result["recipes"]

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    
@router.get("/flavourmarks", response_model=List[RecipeDatabaseOut])
async def get_user_flavourmarks(response: Response, page=1, user_id: str = Depends(validate_token)):
    try:
        result = await get_flavourmarked_recipes(page, user_id)
        response.headers["X-Total-Count"] = str(result["count"])

        return result["recipes"]

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())

@router.get("/{recipe_id}", response_model=RecipeDatabaseOut)
async def get_one(recipe_id, request: Request):
    try:
        user_id = validate_token_unhandled(request)

        recipe = await get_recipe(recipe_id, user_id)

        return recipe

    except RecipeNotFoundException as e:
        logger.info(e)
        raise HTTPException(status_code=404, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())

@router.post("/create")
async def create_recipe(recipe_data: Recipe = Body(...), user_id: str = Depends(validate_token)
):
    try:
        recipe_database_in = RecipeDatabaseIn(
            recipe_name=recipe_data.recipe_name,
            recipe_description=recipe_data.recipe_description,
            ingredients=recipe_data.ingredients,
            steps=recipe_data.steps,
            total_time=recipe_data.total_time,
            difficulty=recipe_data.difficulty,
            servings=recipe_data.servings,
            image_files=recipe_data.image_files,
            created_by=PydanticObjectId(user_id),
            created_date= datetime.now(),
            last_updated_by=PydanticObjectId(user_id),
            last_updated_date=datetime.now())

        recipe_id = await insert_recipe(recipe_database_in.model_dump())
        if (recipe_id is not None):
            return SuccessOut(message="Recipe created successfully", payload={"recipe_id": recipe_id})
        else:
            return ErrorOut(message="Failed to create the recipe")
        
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=ErrorOut(message=str(e)).model_dump())

@router.post("/update/{recipe_id}", response_model=SuccessOut)
async def update_recipe(recipe_id: str, recipe_data: Recipe = Body(...), user_id: str = Depends(validate_token)
):
    try:
        existing_recipe = await get_recipe(recipe_id)

        if user_id != str(existing_recipe['created_by']):
            raise UnauthorisedRecipeModificationException(existing_recipe['recipe_name'])

        existing_image_urls = existing_recipe.get("image_files", [])

        updated_image_urls = recipe_data.image_files

        images_to_delete = list(set(existing_image_urls) - set(updated_image_urls))
        
        image_delete_success = False
        if images_to_delete:
            image_delete_success = await delete_cloudinary_images(images_to_delete)
        
        if not images_to_delete or (images_to_delete and image_delete_success):
            recipe_database_update = RecipeDatabaseUpdate(
                recipe_id = recipe_id,
                recipe_name=recipe_data.recipe_name,
                recipe_description=recipe_data.recipe_description,
                ingredients=recipe_data.ingredients,
                steps=recipe_data.steps,
                total_time=recipe_data.total_time,
                difficulty=recipe_data.difficulty,
                servings=recipe_data.servings,
                image_files=recipe_data.image_files,
                last_updated_by=PydanticObjectId(user_id),
                last_updated_date=datetime.now())
            
            update_success = await update_one_recipe(recipe_database_update)
            if (update_success):
                return SuccessOut(message="Recipe updated successfully")
            else:
                return ErrorOut(message="Failed to update the recipe")
        else:
            if not image_delete_success:
                return ErrorOut(message="Failed to delete cloud images")
            else:
                return ErrorOut(message="Failed to update the recipe")
                       
    except InvalidRecipeIDException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except RecipeNotFoundException as e:
        logger.info(e)
        raise HTTPException(status_code=404, detail=ErrorOut(message=str(e)).model_dump())
    except UnauthorisedRecipeModificationException as e:
        logger.info(e)
        raise HTTPException(status_code=403, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())
    
@router.post("/{recipe_id}/flavourmark", response_model=SuccessOut)
async def toggle_flavourmark(recipe_id: str, user_id: str = Depends(validate_token)
):
    try:
        result = await toggle_recipe_flavourmark(recipe_id, user_id)

        if result:
            return SuccessOut(message="Flavourmark for recipe toggled successfully")
        else:
            return ErrorOut(message="Failed to toggle flavourmark for recipe")
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())

@router.post("/delete/{recipe_id}", response_model=SuccessOut)
async def delete_recipe(recipe_id: str, user_id: str = Depends(validate_token)
):
    try:
        existing_recipe = await get_recipe(recipe_id)

        if user_id != str(existing_recipe['created_by']):
            raise UnauthorisedRecipeModificationException(existing_recipe['recipe_name'])

        existing_image_urls = existing_recipe.get("image_files", [])
        image_delete_success, delete_reviews_success, delete_flavourmark_success,\
        delete_recipe_success = False, False, False, False
        if existing_image_urls:
            image_delete_success = await delete_cloudinary_images(existing_image_urls)

        review_count = await get_reviews_count(recipe_id)
        if review_count > 0:
            delete_reviews_success = await delete_recipe_reviews(recipe_id)

        flavourmark_count = await get_flavourmarks_count(recipe_id)
        if flavourmark_count > 0:
            delete_flavourmark_success = await delete_recipe_flavourmarks(recipe_id)

        delete_recipe_success = await delete_one_recipe(recipe_id)

        if image_delete_success and (review_count == 0 or delete_reviews_success) and\
            (flavourmark_count == 0 or delete_flavourmark_success) and delete_recipe_success:
            return SuccessOut(message="Recipe deleted successfully")
        else:
            return ErrorOut(message="Failed to delete the recipe")
        
    except InvalidRecipeIDException as e:
        logger.info(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except RecipeNotFoundException as e:
        logger.info(e)
        raise HTTPException(status_code=404, detail=ErrorOut(message=str(e)).model_dump())
    except UnauthorisedRecipeModificationException as e:
        logger.info(e)
        raise HTTPException(status_code=403, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message="An unknown error has occurred").model_dump())