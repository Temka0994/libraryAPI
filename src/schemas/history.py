from pydantic import BaseModel


class HistorySchema(BaseModel):
    user_id: int
    book_id: int
