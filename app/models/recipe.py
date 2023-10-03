from pydantic import BaseModel, validator, Field
from fastapi import HTTPException, UploadFile
from typing import Optional, List
from models.response import ErrorOut
from utils.validator import validate_max_length, validate_alphanumeric_symbols, validate_number, validate_filename, validate_content_type, validate_display_name
from utils.annotations import PydanticObjectId
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

class RecipeCreate(BaseModel):
    recipe_name: str
    recipe_description: str
    ingredients: str
    steps: str
    total_time: str
    difficulty: str
    image_name: Optional[str] = None
    image_file: Optional[UploadFile] = None
    created_by: str


    @validator("recipe_name")
    def validate_recipe_name(cls, value):
        max_length = 30
        if not validate_max_length(value, max_length):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Recipe name exceeds the maximum length of '{max_length}'").model_dump())
        return value

    @validator("recipe_description")
    def validate_recipe_description(cls, value):
        max_length = 1000
        if not validate_max_length(value, max_length):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Description exceeds the maximum length of '{max_length}'").model_dump())
        return value

    @validator("ingredients")
    def validate_ingredients(cls, value):
        if not validate_alphanumeric_symbols(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid ingredients").model_dump())
        return value

    @validator("steps")
    def validate_steps(cls, value):
        if not validate_alphanumeric_symbols(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid steps").model_dump())
        return value

    @validator("total_time")
    def validate_total_time(cls, value):
        if not validate_alphanumeric_symbols(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid total time").model_dump())
        return value

    @validator("difficulty")
    def validate_difficulty(cls, value):
        if not validate_number(value) or float(value) < 0 or float(value) > 10:
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid difficulty").model_dump())
        return float(value)

    @validator("image_name")
    def validate_image_name(cls, value):
        if value is None:
            return None
        if not validate_filename(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid image name").model_dump())
        return value
    
    @validator("image_file", pre=True)
    def validate_image_file(cls, value):
        if value is None:
            return None
        if not validate_content_type(value.content_type):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid file type").model_dump())
    
        max_file_size = 10 * 1024 * 1024 ## 10 MB
        if validate_max_length(len(value.file.read()), max_file_size):
            raise HTTPException(status_code=400, detail=ErrorOut(message="File size exceeds the maximum allowed").model_dump())
        return value

    @validator("created_by")
    def validate_created_by(cls, value):
        if not validate_display_name(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid created by").model_dump())
        return value

class RecipeDatabaseIn(BaseModel):
    recipe_name: str
    recipe_description: str
    ingredients: str
    steps: str
    total_time: str
    difficulty: str
    image_name: Optional[str] = None
    image_file: Optional[UploadFile] = None
    created_by: str
    created_date: str
    last_updated_by: str
    last_updated_date: str

    @validator("recipe_name")
    def validate_recipe_name(cls, value):
        if not validate_display_name(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid recipe name").model_dump())
        return value

    @validator("recipe_description")
    def validate_recipe_description(cls, value):
        if not validate_alphanumeric_symbols(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid recipe description").model_dump())
        return value

    @validator("ingredients")
    def validate_ingredients(cls, value):
        if not validate_alphanumeric_symbols(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid ingredients").model_dump())
        return value

    @validator("steps")
    def validate_steps(cls, value):
        if not validate_alphanumeric_symbols(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid steps").model_dump())
        return value

    @validator("total_time")
    def validate_total_time(cls, value):
        if not validate_alphanumeric_symbols(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid total time").model_dump())
        return value

    @validator("difficulty")
    def validate_difficulty(cls, value):
        if not validate_number(value) or float(value) < 0 or float(value) > 10:
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid difficulty").model_dump())
        return float(value)

    @validator("image_name")
    def validate_image_name(cls, value):
        if value is None:
            return None
        if not validate_filename(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid image name").model_dump())
        return value
    
    @validator("image_file", pre=True)
    def validate_image_file(cls, value):
        if value is None:
            return None
        if not validate_content_type(value.content_type):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid file type").model_dump())
    
        max_file_size = 10 * 1024 * 1024 ## 10 MB
        if validate_max_length(len(value.file.read()), max_file_size):
            raise HTTPException(status_code=400, detail=ErrorOut(message="File size exceeds the maximum allowed").model_dump())
        return value

    
    @validator("created_by")
    def validate_created_by(cls, value):
        if not validate_display_name(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid created by").model_dump())
        return value

    @validator("last_updated_by")
    def validate_last_updated_by(cls, value):
        if not validate_display_name(value):
            raise HTTPException(status_code=400, detail=ErrorOut(message="Invalid last updated by").model_dump())
        return value

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