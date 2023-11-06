from pydantic import BaseModel, validator, Field
from typing import List
from utils.validator import *
from utils.annotations import PydanticObjectId
from api.routes.file_route import is_valid_cloudinary_image
from datetime import datetime
from enum import Enum

class FieldName(Enum):
    RECIPE_ID = "Recipe ID"
    RECIPE_NAME = "Recipe name"
    RECIPE_DESCRIPTION = "Description"
    INGREDIENT = "Ingredient"
    STEP = "Step"
    TOTAL_TIME = "Total time"
    DIFFICULTY = "Difficulty"
    SERVINGS = "Servings"
    IMAGE_FILES = "Image file"

class Recipe(BaseModel):
    recipe_name: str
    recipe_description: str
    ingredients: List[str]
    steps: List[str]
    total_time: int
    difficulty: str
    servings: int
    image_files: List[str]

    @validator("recipe_name")
    def validate_recipe_name(cls, value):
        validate_required(FieldName.RECIPE_NAME.value, value)
        validate_invalid(FieldName.RECIPE_NAME.value, value, validate_func=validate_recipe_name)
        return value

    @validator("recipe_description")
    def validate_recipe_description(cls, value):
        validate_required(FieldName.RECIPE_DESCRIPTION.value, value)
        validate_invalid(FieldName.RECIPE_DESCRIPTION.value, value, validate_func=validate_description)
        return value

    @validator("ingredients")
    def validate_ingredients(cls, value):
        for ingredient in value:
            validate_required(FieldName.INGREDIENT.value, ingredient)
            validate_invalid(FieldName.INGREDIENT.value, ingredient, validate_func=validate_ingredient)
        return value

    @validator("steps")
    def validate_steps(cls, value):
        for step in value:
            validate_required(FieldName.STEP.value, step)
            validate_invalid(FieldName.STEP.value, step, validate_func=validate_step)
        return value

    @validator("total_time")
    def validate_total_time(cls, value):
        validate_required_integer(FieldName.TOTAL_TIME.value, value)
        total_time = validate_integer(FieldName.TOTAL_TIME.value, value)
        validate_invalid(FieldName.TOTAL_TIME.value, str(total_time), validate_func=validate_total_time)
        return total_time
    
    @validator("difficulty")
    def validate_difficulty(cls, value):
        validate_required(FieldName.DIFFICULTY.value, value)
        validate_invalid(FieldName.DIFFICULTY.value, value, validate_func=validate_difficulty)
        return value
    
    @validator("servings")
    def validate_servings(cls, value):
        validate_required_integer(FieldName.SERVINGS.value, value)
        servings = validate_integer(FieldName.SERVINGS.value, value)
        validate_invalid(FieldName.SERVINGS.value, str(servings), validate_func=validate_servings)
        return servings
    
    @validator("image_files")
    def validate_image_files(cls, value):
        validate_max_images(FieldName.IMAGE_FILES.value, len(value))
        for image_url in value:
            validate_required(FieldName.IMAGE_FILES.value, image_url)
            validate_invalid(FieldName.IMAGE_FILES.value, image_url, validate_func=is_valid_cloudinary_image)
        return value

class RecipeDatabaseIn(Recipe):
    created_by: PydanticObjectId
    created_date: datetime
    last_updated_by: PydanticObjectId
    last_updated_date: datetime

class RecipeDatabaseOut(RecipeDatabaseIn):
    id: PydanticObjectId = Field(alias="_id")
    flavourmarks_count: int = None
    is_flavourmarked: bool = None

class RecipeDatabaseUpdate(Recipe):
    recipe_id: PydanticObjectId
    last_updated_by: PydanticObjectId
    last_updated_date: datetime

    @validator("recipe_id")
    def validate_recipe_id(cls, value):
        validate_required(FieldName.RECIPE_ID.value, str(value))
        return value