from enum import Enum


class BookState(str, Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"
