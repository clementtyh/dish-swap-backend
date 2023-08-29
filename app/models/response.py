from pydantic import BaseModel
from typing import Optional


class SuccessOut(BaseModel):
    status: str = "success"
    message: Optional[str] = None
    payload: Optional[dict] = None


class ErrorOut(BaseModel):
    status: str = "error"
    message: str = "An unknown error has occurred"
