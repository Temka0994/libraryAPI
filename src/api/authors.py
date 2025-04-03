from fastapi import HTTPException, APIRouter
from sqlalchemy import select

from src.database import SessionDepend
from src.models.authors import AuthorModel
from src.models.books import BookModel
from src.schemas.authors import AuthorSchema, AuthorDateSchema

router = APIRouter()


@router.get('/authors/{id}/books')
async def get_author(new_session: SessionDepend, id: int):
    query = select(BookModel).where(BookModel.author_id == id)
    result = await new_session.execute(query)
    author = result.scalars().all()

    if not author:
        raise HTTPException(status_code=400, detail="There are no authors with this ID.")

    return author


@router.post('/authors')
async def add_author(new_session: SessionDepend, data: AuthorDateSchema):
    new_author = AuthorModel(
        first_name=data.first_name,
        last_name=data.last_name,
        birth_date=data.birth_date
    )

    author_query = select(AuthorModel).where(
        (AuthorModel.first_name == new_author.first_name) &
        (AuthorModel.last_name == new_author.last_name))
    author_result = await new_session.execute(author_query)
    author = author_result.scalar_one_or_none()

    if author:
        raise HTTPException(status_code=400, detail="The author has not been added. He was added earlier.")

    new_session.add(new_author)
    await new_session.commit()

    return {"message": "Author added successfully."}
