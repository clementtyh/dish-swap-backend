from fastapi import APIRouter, HTTPException
from models.response import ErrorOut
from services.recipe_services import get_recipes, get_recipe
from exceptions.recipe_exceptions import RecipeNotFoundException

router = APIRouter()

@router.get("/")
async def root():
    return {"route": "recipe"}

@router.get("/all/{page}")
async def getAll(page):
    try:
        recipes = await get_recipes(page)

        return recipes

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
