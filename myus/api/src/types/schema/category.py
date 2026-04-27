from pydantic import BaseModel


class CategoryOut(BaseModel):
    ulid: str
    jp_name: str
    en_name: str
