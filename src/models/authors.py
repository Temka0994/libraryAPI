from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date
from datetime import date

from src.models.dependencies import Base


class AuthorModel(Base):
    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    birth_date: Mapped[date] = mapped_column(Date)
