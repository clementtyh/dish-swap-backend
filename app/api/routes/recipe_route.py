from fastapi import APIRouter, HTTPException
from models.response import ErrorOut
from services.recipe_services import get_recipes

router = APIRouter()

@router.get("/")
async def root():
    return {"route": "recipe"}

@router.get("/all/{page}")
async def root(page):
    try:
        recipes = await get_recipes(page)

        return recipes

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
