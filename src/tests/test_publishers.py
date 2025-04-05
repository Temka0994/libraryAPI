import pytest
from sqlalchemy import null

from fixture import client


@pytest.mark.asyncio(loop_scope="session")
async def test_success_get_publishers(client):
    response = await client.get("/publishers/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "validation_year": "2005-12-01",
            "publisher_id": 1,
            "name": "Penguin Books"
        },
        {
            "validation_year": "2012-07-03",
            "publisher_id": 2,
            "name": "Bloomsbury Publishing"
        },
        {
            "validation_year": "2017-05-30",
            "publisher_id": 3,
            "name": "HarperCollins"
        },
        {
            "validation_year": "2024-11-12",
            "publisher_id": 4,
            "name": "Houghton Mifflin Harcourt"
        },
        {
            "validation_year": null,
            "publisher_id": 5,
            "name": "Test1"
        },
        {
            "validation_year": null,
            "publisher_id": 6,
            "name": "123"
        },
        {
            "validation_year": null,
            "publisher_id": 7,
            "name": "Testt"
        },
        {
            "validation_year": null,
            "publisher_id": 8,
            "name": "bobbad"
        },
        {
            "validation_year": "2022-04-05",
            "publisher_id": 9,
            "name": "piblis"
        }
    ]


@pytest.mark.asyncio(loop_scope="session")
async def test_add_publisher(client):
    payload = {
        "name": "puslisherTest",
        "validation_year": "2020-02-02"
    }
    response = await client.post("/genres/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Publisher added successfully."}


@pytest.mark.asyncio(loop_scope="session")
async def test_add_publisher_again(client):
    payload = {
        "name": "puslisherTest"
    }
    response = await client.post("/genres/", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "You can not perform this action. Publisher was added earlier."}
