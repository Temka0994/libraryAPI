import pytest
from fixture import client


@pytest.mark.asyncio(loop_scope="session")
async def test_success_get_genres(client):
    response = await client.get("/genres/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Dystopian",
            "genre_id": 1
        },
        {
            "name": "Fantasy",
            "genre_id": 2
        },
        {
            "name": "Adventure",
            "genre_id": 3
        },
        {
            "name": "Classics",
            "genre_id": 4
        },
        {
            "name": "Science Fiction",
            "genre_id": 5
        },
        {
            "name": "Mystery",
            "genre_id": 6
        },
        {
            "name": "Romance",
            "genre_id": 7
        },
        {
            "name": "Historical Fiction",
            "genre_id": 8
        },
        {
            "name": "Horror",
            "genre_id": 9
        },
        {
            "name": "Thriller",
            "genre_id": 10
        },
        {
            "name": "GenreTest",
            "genre_id": 11
        },
        {
            "name": "stringTest",
            "genre_id": 12
        },
        {
            "name": "123123123123213",
            "genre_id": 13
        },
        {
            "name": "string",
            "genre_id": 14
        }
    ]


@pytest.mark.asyncio(loop_scope="session")
async def test_add_genre(client):
    payload = {
        "name": "genreForTest"
    }
    response = await client.post("/genres/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Genre added successfully."}


@pytest.mark.asyncio(loop_scope="session")
async def test_add_genre_again(client):
    payload = {
        "name": "genreForTest"
    }
    response = await client.post("/genres/", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "You can not perform this action. Genre was added earlier."}
