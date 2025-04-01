from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Date, Integer, Text, UniqueConstraint
from datetime import date


class Base(DeclarativeBase):
    pass


class AuthorModel(Base):
    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    birth_date: Mapped[date] = mapped_column(Date)


class PublisherModel(Base):
    __tablename__ = "publishers"

    publisher_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class GenreModel(Base):
    __tablename__ = "genres"

    genre_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class BookModel(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.author_id", ondelete="CASCADE"))
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publishers.publisher_id", ondelete="SET NULL"))
    publish_date: Mapped[date] = mapped_column(Date)


class BookGenreModel(Base):
    __tablename__ = "book_genre"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id", ondelete="CASCADE"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.genre_id", ondelete="CASCADE"), primary_key=True)

    __table_args__ = (UniqueConstraint("book_id", "genre_id", name="uq_book_genre"),)


class StorageModel(Base):
    __tablename__ = "storage"

    storage_id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id", ondelete="CASCADE"))
    count: Mapped[int] = mapped_column(Integer)


class UserModel(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    birth_date: Mapped[date] = mapped_column(Date)
    email: Mapped[str] = mapped_column(String(80))
    password: Mapped[str] = mapped_column(Text)


class HistoryModel(Base):
    __tablename__ = "history"

    history_id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    operation: Mapped[str] = mapped_column(String(50))
