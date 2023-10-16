from pydantic import BaseModel, validator, Field
from fastapi import HTTPException
from typing import List, Union
from models.response import ErrorOut
from utils.validator import *
from utils.annotations import PydanticObjectId
from api.routes.file_route import is_valid_cloudinary_image
import datetime

class RecipeCreate(BaseModel):
    recipe_name: str
    recipe_description: str
    ingredients: List[str]
    steps: List[str]
    total_time: Union [int, str]
    difficulty: str
    servings: Union [int, str]
    image_files: List[str]

    @validator("recipe_name")
    def validate_recipe_name(cls, value):
        if value is None or not value.strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Recipe name is required").model_dump())        
        if not validate_recipe_name(value):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid recipe name '{value}'").model_dump())
        return value

    @validator("recipe_description")
    def validate_recipe_description(cls, value):
        if value is None or not value.strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Description is required").model_dump())
        if not validate_description(value):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid description '{value}'").model_dump())
        return value

    @validator("ingredients")
    def validate_ingredients(cls, value):
        if not value or all(ingredient is None or not ingredient.strip() for ingredient in value):
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Ingredient is required").model_dump())   
        for ingredient in value:
            if not validate_ingredient(ingredient):
                raise HTTPException(
                status_code=400,
                detail=ErrorOut(message=f"Invalid ingredient '{ingredient}'").model_dump())
        return value

    @validator("steps")
    def validate_steps(cls, value):
        if not value or all(step is None or not step.strip() for step in value):
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Step is required").model_dump())   
        for step in value:
            if not validate_step(step):
                raise HTTPException(
                status_code=400,
                detail=ErrorOut(message=f"Invalid step '{step}'").model_dump())
        return value

    @validator("total_time")
    def validate_total_time(cls, value):
        if value is None or not str(value).strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Total time is required").model_dump())
        try:
            total_time = int(value)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Total time must be a valid integer").model_dump()
            ) 
        if not validate_total_time(str(total_time)):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid total time '{total_time}'").model_dump())
        return total_time

    @validator("difficulty")
    def validate_difficulty(cls, value):
        if value is None or not value.strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Difficulty is required").model_dump())   
        if not validate_difficulty(value):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid difficulty '{value}'").model_dump())
        return value

    @validator("servings")
    def validate_servings(cls, value):
        if value is None or not str(value).strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Servings is required").model_dump()) 
        try:
            servings = int(value)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Servings must be a valid integer").model_dump()
            )
        if not validate_servings(str(servings)):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid servings '{servings}'").model_dump())
        return servings
    
    @validator("image_files")
    def validate_image_files(cls, value):
        if not value or all(image_url is None or not image_url.strip() for image_url in value):
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Image file is required").model_dump()) 
        for image_url in value:
            if not is_valid_cloudinary_image(image_url):
                raise HTTPException(
                    status_code=400,
                    detail=ErrorOut(message=f"Invalid image url '{image_url}'").model_dump())
        return value

class RecipeUpdate(BaseModel):
    recipe_id: str
    recipe_name: str
    recipe_description: str
    ingredients: List[str]
    steps: List[str]
    total_time: Union [int, str]
    difficulty: str
    servings: Union [int, str]
    image_files: List[str]

    @validator("recipe_id")
    def validate_recipe_id(cls, value):
        if value is None or not value.strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Recipe ID is required").model_dump())
        return value
    
    @validator("recipe_name")
    def validate_recipe_name(cls, value):
        if value is None or not value.strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Recipe name is required").model_dump())        
        if not validate_recipe_name(value):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid recipe name '{value}'").model_dump())
        return value

    @validator("recipe_description")
    def validate_recipe_description(cls, value):
        if value is None or not value.strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Description is required").model_dump())
        if not validate_description(value):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid description '{value}'").model_dump())
        return value

    @validator("ingredients")
    def validate_ingredients(cls, value):
        if not value or all(ingredient is None or not ingredient.strip() for ingredient in value):
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Ingredient is required").model_dump())   
        for ingredient in value:
            if not validate_ingredient(ingredient):
                raise HTTPException(
                status_code=400,
                detail=ErrorOut(message=f"Invalid ingredient '{ingredient}'").model_dump())
        return value

    @validator("steps")
    def validate_steps(cls, value):
        if not value or all(step is None or not step.strip() for step in value):
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Step is required").model_dump())   
        for step in value:
            if not validate_step(step):
                raise HTTPException(
                status_code=400,
                detail=ErrorOut(message=f"Invalid step '{step}'").model_dump())
        return value

    @validator("total_time")
    def validate_total_time(cls, value):
        if value is None or not str(value).strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Total time is required").model_dump())
        try:
            total_time = int(value)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Total time must be a valid integer").model_dump()
            ) 
        if not validate_total_time(str(total_time)):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid total time '{total_time}'").model_dump())
        return total_time

    @validator("difficulty")
    def validate_difficulty(cls, value):
        if value is None or not value.strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Difficulty is required").model_dump())   
        if not validate_difficulty(value):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid difficulty '{value}'").model_dump())
        return value

    @validator("servings")
    def validate_servings(cls, value):
        if value is None or not str(value).strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Servings is required").model_dump()) 
        try:
            servings = int(value)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Servings must be a valid integer").model_dump()
            )
        if not validate_servings(str(servings)):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid servings '{servings}'").model_dump())
        return servings
    
    @validator("image_files")
    def validate_image_files(cls, value):
        if not value or all(image_url is None or not image_url.strip() for image_url in value):
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Image file is required").model_dump()) 
        for image_url in value:
            if not is_valid_cloudinary_image(image_url):
                raise HTTPException(
                    status_code=400,
                    detail=ErrorOut(message=f"Invalid image url '{image_url}'").model_dump())
        return value


class RecipeDatabaseIn(BaseModel):
    recipe_name: str
    recipe_description: str
    ingredients: List[str]
    steps: List[str]
    total_time: int
    difficulty: str
    servings: int
    image_files: List[str]
    created_by: PydanticObjectId
    created_date: datetime.datetime
    last_updated_by: PydanticObjectId
    last_updated_date: datetime.datetime

    @validator("recipe_name")
    def validate_recipe_name(cls, value):
        if value is None or not value.strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Recipe name is required").model_dump())        
        if not validate_recipe_name(value):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid recipe name '{value}'").model_dump())
        return value

    @validator("recipe_description")
    def validate_recipe_description(cls, value):
        if value is None or not value.strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Description is required").model_dump())
        if not validate_description(value):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid description '{value}'").model_dump())
        return value

    @validator("ingredients")
    def validate_ingredients(cls, value):
        if not value or all(ingredient is None or not ingredient.strip() for ingredient in value):
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Ingredient is required").model_dump())   
        for ingredient in value:
            if not validate_ingredient(ingredient):
                raise HTTPException(
                status_code=400,
                detail=ErrorOut(message=f"Invalid ingredient '{ingredient}'").model_dump())
        return value

    @validator("steps")
    def validate_steps(cls, value):
        if not value or all(step is None or not step.strip() for step in value):
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Step is required").model_dump())   
        for step in value:
            if not validate_step(step):
                raise HTTPException(
                status_code=400,
                detail=ErrorOut(message=f"Invalid step '{step}'").model_dump())
        return value

    @validator("total_time")
    def validate_total_time(cls, value):
        if value is None or not str(value).strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Total time is required").model_dump())
        try:
            total_time = int(value)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Total time must be a valid integer").model_dump()
            ) 
        if not validate_total_time(str(total_time)):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid total time '{total_time}'").model_dump())
        return total_time

    @validator("difficulty")
    def validate_difficulty(cls, value):
        if value is None or not value.strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Difficulty is required").model_dump())   
        if not validate_difficulty(value):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid difficulty '{value}'").model_dump())
        return value

    @validator("servings")
    def validate_servings(cls, value):
        if value is None or not str(value).strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Servings is required").model_dump()) 
        try:
            servings = int(value)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Servings must be a valid integer").model_dump()
            )
        if not validate_servings(str(servings)):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid servings '{servings}'").model_dump())
        return servings
    
    @validator("image_files")
    def validate_image_files(cls, value):
        if not value or all(image_url is None or not image_url.strip() for image_url in value):
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Image file is required").model_dump()) 
        for image_url in value:
            if not is_valid_cloudinary_image(image_url):
                raise HTTPException(
                    status_code=400,
                    detail=ErrorOut(message=f"Invalid image url '{image_url}'").model_dump())
        return value
    
class RecipeDatabaseOut(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    recipe_name: str
    recipe_description: str
    ingredients: List[str]
    steps: List[str]
    total_time: int
    difficulty: str
    servings: int
    image_files: List[str]
    created_by: PydanticObjectId
    created_date: datetime.datetime
    last_updated_by: PydanticObjectId
    last_updated_date: datetime.datetime

class RecipeDatabaseUpdate(BaseModel):
    recipe_id: str
    recipe_name: str
    recipe_description: str
    ingredients: List[str]
    steps: List[str]
    total_time: int
    difficulty: str
    servings: int
    image_files: List[str]
    last_updated_by: PydanticObjectId
    last_updated_date: datetime.datetime

    @validator("recipe_id")
    def validate_recipe_id(cls, value):
        if value is None or not value.strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Recipe ID is required").model_dump())
        return value
    
    @validator("recipe_name")
    def validate_recipe_name(cls, value):
        if value is None or not value.strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Recipe name is required").model_dump())        
        if not validate_recipe_name(value):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid recipe name '{value}'").model_dump())
        return value

    @validator("recipe_description")
    def validate_recipe_description(cls, value):
        if value is None or not value.strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Description is required").model_dump())
        if not validate_description(value):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid description '{value}'").model_dump())
        return value

    @validator("ingredients")
    def validate_ingredients(cls, value):
        if not value or all(ingredient is None or not ingredient.strip() for ingredient in value):
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Ingredient is required").model_dump())   
        for ingredient in value:
            if not validate_ingredient(ingredient):
                raise HTTPException(
                status_code=400,
                detail=ErrorOut(message=f"Invalid ingredient '{ingredient}'").model_dump())
        return value

    @validator("steps")
    def validate_steps(cls, value):
        if not value or all(step is None or not step.strip() for step in value):
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Step is required").model_dump())   
        for step in value:
            if not validate_step(step):
                raise HTTPException(
                status_code=400,
                detail=ErrorOut(message=f"Invalid step '{step}'").model_dump())
        return value

    @validator("total_time")
    def validate_total_time(cls, value):
        if value is None or not str(value).strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Total time is required").model_dump())
        try:
            total_time = int(value)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Total time must be a valid integer").model_dump()
            ) 
        if not validate_total_time(str(total_time)):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid total time '{total_time}'").model_dump())
        return total_time

    @validator("difficulty")
    def validate_difficulty(cls, value):
        if value is None or not value.strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Difficulty is required").model_dump())   
        if not validate_difficulty(value):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid difficulty '{value}'").model_dump())
        return value

    @validator("servings")
    def validate_servings(cls, value):
        if value is None or not str(value).strip():
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Servings is required").model_dump()) 
        try:
            servings = int(value)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Servings must be a valid integer").model_dump()
            )
        if not validate_servings(str(servings)):
            raise HTTPException(
                status_code=400, 
                detail=ErrorOut(message=f"Invalid servings '{servings}'").model_dump())
        return servings
    
    @validator("image_files")
    def validate_image_files(cls, value):
        if not value or all(image_url is None or not image_url.strip() for image_url in value):
            raise HTTPException(
                status_code=400,
                detail=ErrorOut(message="Image file is required").model_dump()) 
        for image_url in value:
            if not is_valid_cloudinary_image(image_url):
                raise HTTPException(
                    status_code=400,
                    detail=ErrorOut(message=f"Invalid image url '{image_url}'").model_dump())
        return value