from fastapi import APIRouter, HTTPException
from src.database import SessionDepend
from sqlalchemy import select
from src.models.publishers import PublisherModel
from src.schemas.publishers import PublisherDateSchema

router = APIRouter(tags=["Publishers"])


@router.get('/publishers/', summary="Gets a list of publishers.")
async def get_publishers(new_session: SessionDepend):
    query = select(PublisherModel)
    result = await new_session.execute(query)
    publishers = result.scalars().all()

    return publishers


@router.post('/publishers/', summary="Add a new publisher.")
async def post_publishers(new_session: SessionDepend, data: PublisherDateSchema):
    query = select(PublisherModel).where(PublisherModel.name == data.name)
    result = await new_session.execute(query)
    publisher = result.scalars().all()

    if publisher:
        raise HTTPException(status_code=400, detail="You can not perform this action. Publisher was added earlier.")

    new_genre = PublisherModel(
        name=data.name,
        validation_year=data.validation_year
    )

    new_session.add(new_genre)
    await new_session.commit()

    return {"message": "Publisher added successfully."}
