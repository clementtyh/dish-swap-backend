from pydantic import BaseModel, validator, Field
from typing import Union
from utils.validator import *
from utils.annotations import PydanticObjectId
from datetime import datetime
from enum import Enum

class Creator(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    display_name: str

class Recipe(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    recipe_name: str

class FieldName(Enum):
    REVIEW_TEXT = "Review text"
    REVIEW_RATING = "Rating"
    RECIPE_ID = "Recipe ID"

class Review(BaseModel):
    text: str
    rating: int
    recipe_id: PydanticObjectId

    @validator("text")
    def validate_text(cls, value):
        validate_required(FieldName.REVIEW_TEXT.value, value)
        validate_invalid(FieldName.REVIEW_TEXT.value, value, validate_func=validate_review_text)
        return value

    @validator("rating")
    def validate_rating(cls, value):
        validate_required_integer(FieldName.REVIEW_RATING.value, value)
        rating = validate_integer(FieldName.REVIEW_RATING.value, value)
        validate_invalid(FieldName.REVIEW_RATING.value, str(rating), validate_func=validate_rating)
        return rating
    
    @validator("recipe_id")
    def validate_recipe_id(cls, value):
        validate_required(FieldName.RECIPE_ID.value, str(value))
        return value
    
class ReviewDatabaseIn(Review):
    created_by: PydanticObjectId
    created_date: datetime
    last_updated_by: PydanticObjectId
    last_updated_date: datetime
    
class ReviewDatabaseOut(Review):
    id: PydanticObjectId = Field(alias="_id")
    created_by: Creator
    created_date: datetime
    last_updated_by: PydanticObjectId
    last_updated_date: datetime

class ProfileReviewDatabaseOut(ReviewDatabaseIn):
    id: PydanticObjectId = Field(alias="_id")
    recipe: Recipe