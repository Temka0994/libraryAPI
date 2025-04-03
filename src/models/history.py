from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, ForeignKey
from datetime import date

from src.models.dependencies import Base


class HistoryModel(Base):
    __tablename__ = "history"

    history_id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    operation: Mapped[str] = mapped_column(String(50))
    operation_date: Mapped[date] = mapped_column(Date)
