from fastapi import APIRouter, HTTPException
from src.database import SessionDepend
from sqlalchemy import select
from src.models.genres import GenreModel
from src.schemas.genres import GenreSchema

router = APIRouter()


@router.get('/genres')
async def get_genres(new_session: SessionDepend):
    query = select(GenreModel)
    result = await new_session.execute(query)
    genres = result.scalars().all()

    return genres


@router.post('/genres')
async def post_genre(new_session: SessionDepend, data: GenreSchema):
    query = select(GenreModel).where(GenreModel.name == data.name)
    result = await new_session.execute(query)
    genre = result.scalars().all()

    if genre:
        raise HTTPException(status_code=400, detail="You can not perform this action. Genre was added earlier.")

    new_genre = GenreModel(
        name=data.name
    )

    new_session.add(new_genre)
    await new_session.commit()

    return {"message": "Genre added successfully."}
