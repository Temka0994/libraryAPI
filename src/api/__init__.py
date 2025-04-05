from fastapi import APIRouter
from src.api.books import router as books_router
from src.api.authors import router as authors_router
from src.api.history import router as history_router
from src.api.genres import router as genres_router
from src.api.publishers import router as publisher_router
from src.authentication.users import router as users_router

main_router = APIRouter()

main_router.include_router(books_router)
main_router.include_router(authors_router)
main_router.include_router(history_router)
main_router.include_router(genres_router)
main_router.include_router(publisher_router)
main_router.include_router(users_router)

