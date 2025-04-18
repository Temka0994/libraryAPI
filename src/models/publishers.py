from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date

from src.models.dependencies import Base


class PublisherModel(Base):
    __tablename__ = "publishers"

    publisher_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    validation_year: Mapped[date] = mapped_column(Date)
