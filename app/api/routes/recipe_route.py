from fastapi import APIRouter, HTTPException, Body, Response
from typing import List
import datetime
from services.recipe_services import create_recipe, get_recipes, get_recipe, check_recipe_exist
from exceptions.recipe_exceptions import RecipeNotFoundException, RecipeAlreadyExistsException
from models.response import ErrorOut, SuccessOut
from models.recipe import RecipeCreate, RecipeDatabaseIn, RecipeDatabaseOut

router = APIRouter()

@router.get("/", response_model=List[RecipeDatabaseOut])
async def root(response: Response, page=1):
    try:
        result = await get_recipes(page)
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
async def createRecipe(recipe_data: RecipeCreate = Body(...)):
    try:
        await check_recipe_exist(recipe_data.recipe_name)

        recipe_database_in = RecipeDatabaseIn(
            recipe_name=recipe_data.recipe_name,
            recipe_description=recipe_data.recipe_description,
            ingredients=recipe_data.ingredients,
            steps=recipe_data.steps,
            total_time=recipe_data.total_time,
            difficulty=recipe_data.difficulty,
            image_name=recipe_data.image_name,
            image_file=recipe_data.image_file,
            created_by=recipe_data.created_by,
            created_date= datetime.now(),
            last_updated_by=recipe_data.created_by,
            last_updated_date=datetime.now())

        await create_recipe(recipe_database_in)

        return SuccessOut()
    
    except RecipeAlreadyExistsException as e:
        print(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=ErrorOut(message=str(e)).model_dump())
