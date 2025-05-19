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


book_genre_map = {
    "fiction": "Fiction",
    "nonfiction": "Non-fiction",
    "mystery": "Mystery",
    "thriller": "Thriller",
    "romance": "Romance",
    "science_fiction": "Science Fiction",
    "fantasy": "Fantasy",
    "horror": "Horror",
    "historical_fiction": "Historical Fiction",
    "biography": "Biography",
    "memoir": "Memoir",
    "poetry": "Poetry",
    "young_adult": "Young Adult",
    "childrens": "Children's",
    "adventure": "Adventure",
    "crime_fiction": "Crime Fiction",
    "philosophy": "Philosophy",
    "history": "History",
    "graphic_novel": "Graphic Novel",
}
