import pytest
from fixture import client


@pytest.mark.asyncio(loop_scope="session")
async def test_paginate_books(client):
    response = await client.get("/books/?page=1&size=3")
    assert response.status_code == 200
    assert response.json() == [
        {
            "book_id": 1,
            "author_id": 1,
            "publish_date": "1949-06-08",
            "publisher_id": 1,
            "name": "1984",
            "isbn": "978-0-452-52983-4"
        },
        {
            "book_id": 2,
            "author_id": 2,
            "publish_date": "1997-06-26",
            "publisher_id": 2,
            "name": "Harry Potter and the Sorcerer's Stone",
            "isbn": "978-0-7475-3269-9"
        },
        {
            "book_id": 3,
            "author_id": 3,
            "publish_date": "1937-09-21",
            "publisher_id": 3,
            "name": "The Hobbit",
            "isbn": "978-0-618-96863-3"
        }
    ]


@pytest.mark.asyncio(loop_scope="session")
async def test_paginate_book_sorting_by_author(client):
    response = await client.get("/books/?page=2&size=2&sort_by=author")
    assert response.status_code == 200
    assert response.json() == [
        {
            "author_id": 6,
            "book_id": 14,
            "publish_date": "2024-04-02",
            "publisher_id": 1,
            "name": "goodjob",
            "isbn": "978-3-16-143410-0"
        },
        {
            "author_id": 6,
            "book_id": 12,
            "publish_date": "2024-04-02",
            "publisher_id": 1,
            "name": "goodjob",
            "isbn": "978-3-16-143410-0"
        }
    ]


@pytest.mark.asyncio(loop_scope="session")
async def test_paginate_book_sorting_by_name(client):
    response = await client.get("/books/?page=1&size=3&sort_by=name")
    assert response.status_code == 200
    assert response.json() == [
        {
            "author_id": 1,
            "book_id": 1,
            "publisher_id": 1,
            "name": "1984",
            "publish_date": "1949-06-08",
            "isbn": "978-0-452-52983-4"
        },
        {
            "author_id": 6,
            "book_id": 11,
            "publisher_id": 4,
            "name": "Aboba",
            "publish_date": "2024-04-02",
            "isbn": "111-2-33-138310-0"
        },
        {
            "author_id": 1,
            "book_id": 8,
            "publisher_id": 4,
            "name": "Brave New World",
            "publish_date": "1932-08-01",
            "isbn": "978-0-06-085052-1"
        }
    ]


@pytest.mark.asyncio(loop_scope="session")
async def test_paginate_book_sorting_by_publish_date(client):
    response = await client.get("/books/?page=1&size=3&sort_by=publish_date")
    assert response.status_code == 200
    assert response.json() == [
        {
            "author_id": 1,
            "book_id": 8,
            "publisher_id": 4,
            "name": "Brave New World",
            "publish_date": "1932-08-01",
            "isbn": "978-0-06-085052-1"
        },
        {
            "author_id": 1,
            "book_id": 9,
            "publisher_id": 1,
            "name": "TEST1",
            "publish_date": "1933-04-02",
            "isbn": "978-3-16-148410-0"
        },
        {
            "author_id": 3,
            "book_id": 3,
            "publisher_id": 3,
            "name": "The Hobbit",
            "publish_date": "1937-09-21",
            "isbn": "978-0-618-96863-3"
        }
    ]


@pytest.mark.asyncio(loop_scope="session")
async def test_post_book_success(client):
    payload = {
        "author": {
            "first_name": "Ivan",
            "last_name": "Franko"
        },
        "isbn": "978-3-16-148410-0",
        "name": "Success",
        "publish_date": "2020-02-20",
        "publisher": {
            "name": "Penguin Books"
        }
    }

    response = await client.post("/books/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Book added successfully."}


@pytest.mark.asyncio(loop_scope="session")
async def test_post_book_with_not_exist_publisher(client):
    payload = {
        "author": {
            "first_name": "Ivan",
            "last_name": "Franko"
        },
        "isbn": "978-3-16-148410-0",
        "name": "NoSuccess",
        "publish_date": "2020-02-20",
        "publisher": {
            "name": "Sunny"
        }
    }

    response = await client.post("/books/", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Publisher does not exist."}


@pytest.mark.asyncio(loop_scope="session")
async def test_post_book_with_not_exist_author(client):
    payload = {"author": {
        "first_name": "Fake",
        "last_name": "Franko"
    },
        "isbn": "978-3-16-148410-0",
        "name": "NoSuccess",
        "publish_date": "2020-02-20",
        "publisher": {
            "name": "Penguin Books"
        }
    }

    response = await client.post("/books/", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Author does not exist."}


@pytest.mark.asyncio(loop_scope="session")
async def test_post_book_with_not_correct_isbn(client):
    payload = {
        "author": {
            "first_name": "Ivan",
            "last_name": "Franko"
        },
        "isbn": "93-16-7435-1",
        "name": "NoSuccess",
        "publish_date": "2020-02-20",
        "publisher": {
            "name": "Penguin Books"
        }
    }

    response = await client.post("/books/", json=payload)
    assert response.status_code == 422
    assert "Value error, Invalid ISBN format. Expected ISBN-13 with dashes." in response.text
