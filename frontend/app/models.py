from django.db import models


class BookGenre(models.TextChoices):
    FICTION = "fiction", "Fiction"
    NONFICTION = "nonfiction", "Non-fiction"
    MYSTERY = "mystery", "Mystery"
    THRILLER = "thriller", "Thriller"
    ROMANCE = "romance", "Romance"
    SCIENCE_FICTION = "science_fiction", "Science Fiction"
    FANTASY = "fantasy", "Fantasy"
    HORROR = "horror", "Horror"
    HISTORICAL_FICTION = "historical_fiction", "Historical Fiction"
    BIOGRAPHY = "biography", "Biography"
    MEMOIR = "memoir", "Memoir"
    POETRY = "poetry", "Poetry"
    YOUNG_ADULT = "young_adult", "Young Adult"
    CHILDRENS = "childrens", "Children's"
    ADVENTURE = "adventure", "Adventure"
    CRIME_FICTION = "crime_fiction", "Crime Fiction"
    PHILOSOPHY = "philosophy", "Philosophy"
    HISTORY = "history", "History"
    GRAPHIC_NOVEL = "graphic_novel", "Graphic Novel"


class Status(models.TextChoices):
    TODO = "todo", "To Do"
    READING = "reading", "Reading"
    FINISHED = "finished", "Finished"


class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genres = models.JSONField()  # To store the list of genres
    year = models.IntegerField()
    language = models.CharField(max_length=50)
    pages = models.IntegerField()
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.TODO)

    def __str__(self):
        return f"Book(id={self.id}, title={self.title}, author={self.author})"
