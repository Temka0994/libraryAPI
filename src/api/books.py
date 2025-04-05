from fastapi import APIRouter
from src.database import SessionDepend
from src.enums.books import BookSorting
from src.models.authors import AuthorModel
from src.models.books import BookModel
from typing import Optional
from fastapi import Query, HTTPException
from sqlalchemy import select

from src.models.publishers import PublisherModel
from src.schemas.books import BookSchema

router = APIRouter(tags=["Books"])


@router.get('/books/', summary="Gets a list of books.")
async def get_book(new_session: SessionDepend,
                   page: Optional[int] = Query(None, ge=1),
                   size: Optional[int] = Query(None, ge=1),
                   sort_by: Optional[BookSorting] = None):
    query = select(BookModel).join(AuthorModel, BookModel.author_id == AuthorModel.author_id)

    sort_columns = {
        BookSorting.NAME: BookModel.name,
        BookSorting.AUTHOR: AuthorModel.last_name,
        BookSorting.PUBLISH_DATE: BookModel.publish_date
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


@router.post('/books/', summary="Adds a new book.")
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
