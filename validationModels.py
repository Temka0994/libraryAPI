import datetime
import re

from pydantic import BaseModel, Field, field_validator


class AuthorSchema(BaseModel):
    first_name: str
    last_name: str


class PublisherSchema(BaseModel):
    name: str


class BookSchema(BaseModel):
    name: str
    author: AuthorSchema
    publisher: PublisherSchema
    publish_date: datetime.date
    isbn: str = Field()

    @field_validator("isbn", mode="before")
    def validate_isbn(cls, value: str):
        pattern = r"^(?:\d{1,5}-\d{1,7}-\d{1,7}-[\dX]|\d{3}-\d{1,5}-\d{1,7}-\d{1,7}-[\dX])$"
        if not re.fullmatch(pattern, value):
            raise ValueError("Invalid ISBN format. Expected ISBN-10 or ISBN-13 with dashes.")
        return value

    @field_validator("publish_date", mode='before')
    def date_validation(cls, value):
        value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
        if value > datetime.date.today():
            raise ValueError("Invalid Date format. Check your format and date. Date must be in past.")
        return value

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "author": {
                        "first_name": "Тарас",
                        "last_name": "Шевченко"
                    },
                    "isbn": "978-3-16-148410-0",
                    "name": "Кобзар",
                    "publish_date": "2024-04-02",
                    "publisher": {
                        "name": "Видавництво сонечко"
                    }
                }
            ]
        }
    }
