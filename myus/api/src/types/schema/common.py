from pydantic import BaseModel

class ErrorOut(BaseModel):
    message: str


class MessageOut(BaseModel):
    error: bool
    message: str
