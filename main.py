from typing import Annotated, Optional
from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import select

from libraryModel import BookModel, AuthorModel

DATABASE_URL = "postgresql+asyncpg://admin:root@localhost/library"
app = FastAPI()

engine = create_async_engine(DATABASE_URL)
session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with session() as new_session:
        yield new_session


SessionDepend = Annotated[AsyncSession, Depends(get_session)]


@app.get('/books/')
async def get_book(new_session: SessionDepend,
                   page: Optional[int] = Query(None, ge=1),
                   size: Optional[int] = Query(None, ge=1),
                   sort_by: Optional[str] = None):
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
