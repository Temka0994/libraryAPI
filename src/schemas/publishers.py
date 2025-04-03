from pydantic import BaseModel


class PublisherSchema(BaseModel):
    name: str
