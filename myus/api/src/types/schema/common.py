from pydantic import BaseModel


class ErrorOut(BaseModel):
    message: str
