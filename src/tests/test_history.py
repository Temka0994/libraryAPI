import pytest
from fixture import client


@pytest.mark.asyncio(loop_scope="session")
async def test_success_get_book_history(client):
    response = await client.get("/books/3/history/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "operation_date": "2025-04-03",
            "history_id": 1,
            "book_id": 2,
            "user_id": 1,
            "operation": "borrowed"
        },
        {
            "operation_date": "2025-04-03",
            "history_id": 14,
            "book_id": 2,
            "user_id": 1,
            "operation": "returned"
        },
        {
            "operation_date": "2025-04-05",
            "history_id": 25,
            "book_id": 2,
            "user_id": 1,
            "operation": "borrowed"
        }
    ]


@pytest.mark.asyncio(loop_scope="session")
async def test_not_success_get_book_history(client):
    response = await client.get("/books/400/history/")
    assert response.status_code == 400
    assert response.json() == {"detail": "This book does not have a history."}


@pytest.mark.asyncio(loop_scope="session")
async def test_borrow_book(client):
    payload = {
        "user_id": 3,
        "book_id": 3
    }
    response = await client.post("/borrow/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Book borrowed successfully."}


@pytest.mark.asyncio(loop_scope="session")
async def test_bad_borrow_book(client):
    payload = {
        "user_id": 9,
        "book_id": 100
    }
    response = await client.post("/return/", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "You can not perform this operation."}


@pytest.mark.asyncio(loop_scope="session")
async def test_return_book(client):
    payload = {
        "user_id": 3,
        "book_id": 3
    }
    response = await client.post("/return/", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Book returned successfully."}


@pytest.mark.asyncio(loop_scope="session")
async def test_bad_return_book(client):
    payload = {
        "user_id": 9,
        "book_id": 100
    }
    response = await client.post("/return/", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "You can not perform this operation."}
