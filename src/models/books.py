from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, ForeignKey
from datetime import date

from src.models.dependencies import Base


class BookModel(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.author_id", ondelete="CASCADE"))
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publishers.publisher_id", ondelete="SET NULL"))
    publish_date: Mapped[date] = mapped_column(Date)
    isbn: Mapped[str] = mapped_column(String(17))
