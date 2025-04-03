from enum import Enum


class BookSorting(str, Enum):
    NAME = "name"
    AUTHOR = "author"
    PUBLISH_DATE = "publish_date"
