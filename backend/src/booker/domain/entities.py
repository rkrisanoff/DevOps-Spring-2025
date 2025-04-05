import enum


class BookGenre(enum.StrEnum):
    FICTION = "fiction"
    NONFICTION = "nonfiction"
    MYSTERY = "mystery"
    THRILLER = "thriller"
    ROMANCE = "romance"
    SCIENCE_FICTION = "science_fiction"
    FANTASY = "fantasy"
    HORROR = "horror"
    HISTORICAL_FICTION = "historical_fiction"
    BIOGRAPHY = "biography"
    MEMOIR = "memoir"
    POETRY = "poetry"
    YOUNG_ADULT = "young_adult"
    CHILDRENS = "childrens"
    ADVENTURE = "adventure"
    CRIME_FICTION = "crime_fiction"
    PHILOSOPHY = "philosophy"
    HISTORY = "history"
    GRAPHIC_NOVEL = "graphic_novel"


class Status(enum.StrEnum):
    TODO = "todo"
    READING = "reading"
    FINISHED = "finished"
