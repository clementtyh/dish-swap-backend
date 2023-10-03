from fastapi import APIRouter, HTTPException, Body, Response, Depends
from typing import List
import datetime
from services.auth_services import validate_token
from services.recipe_services import create_recipe, get_recipes, get_recipe, check_recipe_exist, add_flavourmark_recipe, remove_flavourmark_recipe
from exceptions.recipe_exceptions import RecipeNotFoundException, RecipeAlreadyExistsException
from models.response import ErrorOut, SuccessOut
from models.recipe import RecipeCreate, RecipeDatabaseIn, RecipeDatabaseOut

router = APIRouter()

@router.get("/", response_model=List[RecipeDatabaseOut])
async def root(response: Response, page=1, user_id: str = Depends(validate_token)):
    try:
        result = await get_recipes(page, user_id)
        response.headers["X-Total-Count"] = str(result["count"])

        return result["recipes"]

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
    
@router.get("/{id}", response_model=RecipeDatabaseOut)
async def getOne(id, user_id: str = Depends(validate_token)):
    try:
        recipe = await get_recipe(id, user_id)

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
    
@router.post("/add-flavourmark/{id}")
async def addFlavourmark(id, user_id: str = Depends(validate_token)):
    try:
        if not user_id:
            raise HTTPException(status_code=401, detail=ErrorOut(message="Invalid authorization header").model_dump())
        
        await add_flavourmark_recipe(id, user_id)

        return SuccessOut()

    except RecipeNotFoundException as e:
        print(e)
        raise HTTPException(status_code=404, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())

@router.post("/remove-flavourmark/{id}")
async def removeFlavourmark(id, user_id: str = Depends(validate_token)):
    try:
        if not user_id:
            raise HTTPException(status_code=401, detail=ErrorOut(message="Invalid authorization header").model_dump())
        
        await remove_flavourmark_recipe(id, user_id)

        return SuccessOut()

    except RecipeNotFoundException as e:
        print(e)
        raise HTTPException(status_code=404, detail=ErrorOut(message=str(e)).model_dump())
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())