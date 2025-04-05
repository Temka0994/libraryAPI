import pytest
from fixture import client


@pytest.mark.asyncio(loop_scope="session")
async def test_success_get_books(client):
    response = await client.get("/authors/5/books/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "book_id": 5,
            "author_id": 5,
            "publish_date": "1951-06-01",
            "publisher_id": 1,
            "name": "Foundation",
            "isbn": "978-0-553-80371-0"
        }
    ]


@pytest.mark.asyncio(loop_scope="session")
async def test_not_success_get_books(client):
    response = await client.get("/authors/200/books/")
    assert response.status_code == 400
    assert response.json() == {"detail": "There are no authors with this ID."}


@pytest.mark.asyncio(loop_scope="session")
async def test_add_author(client):
    payload = {
        "birth_date": "1933-08-31",
        "first_name": "Robert",
        "last_name": "Adams"
    }
    response = await client.post("/authors/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Author added successfully."}


@pytest.mark.asyncio(loop_scope="session")
async def test_add_author_again(client):
    payload = {
        "birth_date": "1933-08-31",
        "first_name": "Robert",
        "last_name": "Adams"
    }
    response = await client.post("/authors/", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "The author has not been added. He was added earlier."}
