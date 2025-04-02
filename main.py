from enum import Enum
from typing import Annotated, Optional
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import select
from validationModels import BookSchema
from libraryModel import BookModel, AuthorModel, PublisherModel, HistoryModel

DATABASE_URL = "postgresql+asyncpg://admin:root@localhost/library"
app = FastAPI()

engine = create_async_engine(DATABASE_URL)
session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with session() as new_session:
        yield new_session


SessionDepend = Annotated[AsyncSession, Depends(get_session)]


class BookSorting(str, Enum):
    name = "name"
    author = "author"
    publish_date = "publish_date"


@app.get('/books')
async def get_book(new_session: SessionDepend,
                   page: Optional[int] = Query(None, ge=1),
                   size: Optional[int] = Query(None, ge=1),
                   sort_by: Optional[BookSorting] = None):
    query = select(BookModel).join(AuthorModel, BookModel.author_id == AuthorModel.author_id)

    sort_columns = {
        "name": BookModel.name,
        "author": AuthorModel.last_name,
        "publish_date": BookModel.publish_date
    }

    if sort_by in sort_columns:
        query = query.order_by(sort_columns[sort_by])
    else:
        query = query.order_by(BookModel.book_id)

    result = await new_session.execute(query)
    books = result.scalars().all()

    if page and size:
        start_index = (page - 1) * size
        end_index = start_index + size
        books = books[start_index:end_index]

    return books


@app.post('/books')
async def post_book(new_session: SessionDepend, data: BookSchema):
    author_query = select(AuthorModel).where(
        (AuthorModel.first_name == data.author.first_name) &
        (AuthorModel.last_name == data.author.last_name))
    author_result = await new_session.execute(author_query)
    author = author_result.scalar_one_or_none()

    if not author:
        raise HTTPException(status_code=400, detail="Author does not exist.")

    publisher_query = select(PublisherModel).where(
        (PublisherModel.name == data.publisher.name))
    publisher_result = await new_session.execute(publisher_query)
    publisher = publisher_result.scalar_one_or_none()

    if not publisher:
        raise HTTPException(status_code=400, detail="Publisher does not exist.")

    new_book = BookModel(
        name=data.name,
        author_id=author.author_id,
        publisher_id=publisher.publisher_id,
        publish_date=data.publish_date,
        isbn=data.isbn
    )

    new_session.add(new_book)
    await new_session.commit()

    return {"message": "Book added successfully."}


@app.get('/books/{id}/history')
async def get_book_history(new_session: SessionDepend, id: int):
    query = select(HistoryModel).join(BookModel, BookModel.book_id == HistoryModel.book_id).where(
        BookModel.book_id == id)
    result = await new_session.execute(query)
    history = result.scalars().all()

    if not history:
        return {"message": "This book doesn't have a history."}
    return history


@app.get('/authors/{id}/books')
async def get_author(new_session: SessionDepend):
    pass