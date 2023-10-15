from fastapi import APIRouter, HTTPException, Body, Response, Depends
from typing import List
from services.auth_services import validate_token
from services.recipe_services import *
from models.response import ErrorOut, SuccessOut
from models.recipe import *
from exceptions.recipe_exceptions import *
from api.routes.file_route import upload_image_files_to_cloud

router = APIRouter()

@router.get("/", response_model=List[RecipeDatabaseOut])
async def root(response: Response, page=1, search=""):
    try:
        result = await get_recipes(page, search)
        response.headers["X-Total-Count"] = str(result["count"])

        return result["recipes"]

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    
@router.get("/{id}", response_model=RecipeDatabaseOut)
async def getOne(id):
    try:
        recipe = await get_recipe(id)

        return recipe

    except RecipeNotFoundException as e:
        print(e)
        raise HTTPException(status_code=404, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())

@router.post("/create")
async def create_recipe(recipe_data: RecipeCreate = Body(...), user_id: str = Depends(validate_token)
):
    try:
        await check_recipe_exist(recipe_data.recipe_name)

        file_urls = upload_image_files_to_cloud(recipe_data.image_files)

        recipe_database_in = RecipeDatabaseIn(
            recipe_name=recipe_data.recipe_name,
            recipe_description=recipe_data.recipe_description,
            ingredients=recipe_data.ingredients,
            steps=recipe_data.steps,
            total_time=recipe_data.total_time,
            difficulty=recipe_data.difficulty,
            servings=recipe_data.servings,
            image_files=file_urls,
            created_by=user_id,
            created_date= datetime.now(),
            last_updated_by=user_id,
            last_updated_date=datetime.now())
        await insert_recipe(recipe_database_in.model_dump())

        return SuccessOut()
    
    except RecipeAlreadyExistsException as e:
        print(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=ErrorOut(message=str(e)).model_dump())
