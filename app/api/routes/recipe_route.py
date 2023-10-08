from fastapi import APIRouter, HTTPException, Body, Depends
from fastapi.responses import JSONResponse
from models.response import ErrorOut, SuccessOut
from services.recipe_services import *
from exceptions.recipe_exceptions import *
from models.recipe import *
from api.routes.file_route import get_file_url
from services.auth_services import validate_token

router = APIRouter()

@router.get("/")
async def root(page=1):
    try:
        result = await get_recipes(page)
        headers = {"X-Total-Count": str(result["count"])}

        return JSONResponse(content=result["recipes"], headers=headers)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    
@router.get("/{id}")
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
async def create_recipe(recipe_data: RecipeCreate = Body(...), str = Depends(validate_token)
):
    try:
        await check_recipe_exist(recipe_data.recipe_name)

        file_urls = get_file_url(recipe_data.image_files)

        recipe_database_in = RecipeDatabaseIn(
            recipe_name=recipe_data.recipe_name,
            recipe_description=recipe_data.recipe_description,
            ingredients=recipe_data.ingredients,
            steps=recipe_data.steps,
            total_time=recipe_data.total_time,
            difficulty=recipe_data.difficulty,
            servings=recipe_data.servings,
            image_files=file_urls,
            created_by=recipe_data.created_by,
            created_date= datetime.now(),
            last_updated_by=recipe_data.created_by,
            last_updated_date=datetime.now())
        await insert_recipe(recipe_database_in.model_dump())

        return SuccessOut()
    
    except RecipeAlreadyExistsException as e:
        print(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=ErrorOut(message=str(e)).model_dump())
