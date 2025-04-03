import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class AuthorSchema(BaseModel):
    first_name: str
    last_name: str
    birth_date: Optional[datetime.date] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Ivan",
                    "last_name": "Franko",
                    "birth_date": "1856-08-27"
                }
            ]
        }
    }

    @field_validator("birth_date", mode='before')
    def date_validation(cls, value: str):
        value = datetime.date.fromisoformat(value)
        if value > datetime.date.today():
            raise ValueError("Invalid Date format. Check your format and date. Date must be in past.")
        return value
