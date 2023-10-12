from pydantic import BaseModel, Field
from utils.annotations import PydanticObjectId
import datetime

class Test(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    display_name: str

class ReviewDatabaseOut(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    text: str
    rating: int
    recipe_id: PydanticObjectId
    created_by: Test
    created_date: datetime.datetime
    last_updated_by: PydanticObjectId
    last_updated_date: datetime.datetime