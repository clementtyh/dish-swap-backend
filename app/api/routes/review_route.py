from fastapi import APIRouter, HTTPException, Response
from typing import List
from services.review_services import get_reviews
from models.response import ErrorOut
from models.review import ReviewDatabaseOut

router = APIRouter()

@router.get("/", response_model=List[ReviewDatabaseOut])
async def root(response: Response, page=1, recipe=""):
    try:
        result = await get_reviews(page, recipe)
        response.headers["X-Total-Count"] = str(result["count"])

        return result["reviews"]

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=ErrorOut(message=str(e)).model_dump())