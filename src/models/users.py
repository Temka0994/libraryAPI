from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Date

from src.models.dependencies import Base


class UserModel(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    birth_date: Mapped[date] = mapped_column(Date)
    email: Mapped[str] = mapped_column(String(80))
    password: Mapped[str] = mapped_column(Text)
