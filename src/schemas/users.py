import datetime
from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserSchema(LoginSchema):
    first_name: str
    last_name: str
    birth_date: datetime.date
