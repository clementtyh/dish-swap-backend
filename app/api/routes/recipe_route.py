from fastapi import APIRouter, HTTPException, Response
from models.response import ErrorOut
from services.recipe_services import get_recipes, get_recipe
from exceptions.recipe_exceptions import RecipeNotFoundException
from typing import List
from models.recipe import RecipeDatabaseOut

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
