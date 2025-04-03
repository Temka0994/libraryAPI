import datetime

from pydantic import BaseModel, field_validator


class PublisherSchema(BaseModel):
    name: str


class PublisherDateSchema(PublisherSchema):
    validation_year: datetime.date

    @field_validator("validation_year", mode='before')
    def date_validation(cls, value: str):
        value = datetime.date.fromisoformat(value)
        if value > datetime.date.today():
            raise ValueError("Invalid Date format. Check your format and date. Date must be in past.")
        return value
