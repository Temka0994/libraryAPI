from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer

from src.models.dependencies import Base


class StorageModel(Base):
    __tablename__ = "storage"

    storage_id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id", ondelete="CASCADE"))
    count: Mapped[int] = mapped_column(Integer)
