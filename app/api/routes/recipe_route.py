from fastapi import APIRouter, HTTPException

from models.response import SuccessOut, ErrorOut

from services.recipe_services import get_recipes


router = APIRouter()


@router.get("/")
async def root():
    return {"route": "recipe"}


@router.get("/all/{page}")
async def root():
    try:
        recipes = await get_recipes()

        return SuccessOut()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())
