from pydantic import BaseModel, Field
from typing import List
from utils.annotations import PydanticObjectId

class Nutrition(BaseModel):
    calories: str
    protein: str
    fat: str
    carbohydrates: str
    fiber: str
    sugar: str

class Review(BaseModel):
    reviewer: str
    rating: int
    review: str

class RecipeDatabaseOut(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    name: str
    imgPath: str
    description: str
    display_name: str
    ingredients: List[str]
    preparationSteps: List[str]
    nutrition: Nutrition
    difficulty: str
    totalTime: str
    servings: int
    reviews: List[Review]
    flavourmarkCount: int
    flavourmarks: List[PydanticObjectId]    