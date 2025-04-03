from pydantic import BaseModel


class GenreSchema(BaseModel):
    name: str
