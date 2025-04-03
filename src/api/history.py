import datetime
from fastapi import HTTPException, APIRouter
from sqlalchemy import select

from src.constants import ALLOWED_BOOKS_COUNT
from src.database import SessionDepend
from src.enums.history import BookState
from src.models.books import BookModel
from src.models.history import HistoryModel
from src.models.storage import StorageModel
from src.schemas.history import HistorySchema

router = APIRouter()


@router.get('/books/{id}/history')
async def get_book_history(new_session: SessionDepend, id: int):
    query = select(HistoryModel).join(BookModel, BookModel.book_id == HistoryModel.book_id).where(
        BookModel.book_id == id)
    result = await new_session.execute(query)
    history = result.scalars().all()

    if not history:
        raise HTTPException(status_code=400, detail="This book does not have a history.")

    return history


def count_operations(history: list):
    borrowed_count = sum(1 for column in history if column.operation == BookState.BORROWED)
    returned_count = sum(1 for column in history if column.operation == BookState.RETURNED)
    return borrowed_count, returned_count


@router.post('/borrow')
async def borrow_book(new_session: SessionDepend, data: HistorySchema):
    query = select(HistoryModel).where(HistoryModel.user_id == data.user_id)
    history_result = await new_session.execute(query)
    history = history_result.scalars().all()

    borrowed_count, returned_count = count_operations(history)
    books_on_hand = borrowed_count - returned_count

    if books_on_hand >= ALLOWED_BOOKS_COUNT:
        raise HTTPException(status_code=400, detail="You can not have more than three books on hand.")

    query = select(StorageModel).where(StorageModel.book_id == data.book_id)
    storage_result = await new_session.execute(query)
    storage = storage_result.scalar_one_or_none()

    if storage.count == 0:
        raise HTTPException(status_code=400, detail="There are no more of these books left in storage.")

    new_operation = HistoryModel(
        book_id=data.book_id,
        user_id=data.user_id,
        operation=BookState.BORROWED,
        operation_date=datetime.date.today()
    )

    new_session.add(new_operation)
    storage.count -= 1

    await new_session.commit()

    return {"message": "Book borrowed successfully."}


@router.post('/return')
async def return_book(new_session: SessionDepend, data: HistorySchema):
    query = select(HistoryModel).where((HistoryModel.user_id == data.user_id) & (HistoryModel.book_id == data.book_id))
    history_result = await new_session.execute(query)
    history = history_result.scalars().all()

    query_storage = select(StorageModel).where(StorageModel.book_id == data.book_id)
    storage_result = await new_session.execute(query_storage)
    storage = storage_result.scalar_one_or_none()

    borrowed_count, returned_count = count_operations(history)

    if not borrowed_count > returned_count:
        raise HTTPException(status_code=400, detail="You can not perform this operation.")

    new_operation = HistoryModel(
        book_id=data.book_id,
        user_id=data.user_id,
        operation=BookState.RETURNED,
        operation_date=datetime.date.today()
    )

    new_session.add(new_operation)
    storage.count += 1

    await new_session.commit()

    return {"message": "Book returned successfully."}
