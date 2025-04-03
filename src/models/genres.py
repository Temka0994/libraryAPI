from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, UniqueConstraint

from src.models.dependencies import Base


class GenreModel(Base):
    __tablename__ = "genres"

    genre_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class BookGenreModel(Base):
    __tablename__ = "book_genre"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id", ondelete="CASCADE"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.genre_id", ondelete="CASCADE"), primary_key=True)

    __table_args__ = (UniqueConstraint("book_id", "genre_id", name="uq_book_genre"),)
