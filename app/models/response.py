from pydantic import BaseModel
from typing import Optional


class ResponseOut(BaseModel):
    status: str
    message: str


class SuccessOut(ResponseOut):
    status: str = "success"
    message: Optional[str] = None
    payload: Optional[dict] = None


class ErrorOut(ResponseOut):
    status: str = "error"
    message: str = "An unknown error has occurred"
