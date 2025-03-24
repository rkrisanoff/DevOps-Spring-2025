import datetime

import sqlalchemy as sa
from sqlalchemy import BigInteger, Column
from sqlalchemy.ext.declarative import declarative_base

from booker.domain.entities import BookGenre

Base = declarative_base()


class Book(Base):
    __tablename__ = "book"

    id: int = Column(BigInteger, primary_key=True, index=True)
    title: str = Column(
        sa.String,
    )
    author: str = Column(
        sa.String,
    )
    genres: list[BookGenre] = Column(sa.ARRAY(sa.String))
    year: int = Column(
        sa.Integer,
    )
    language: str = Column(
        sa.String,
    )
    pages: int = Column(
        sa.Integer,
    )
    status: str = Column(sa.String, nullable=True)
    created_at = Column(sa.DateTime(timezone=True), default=datetime.datetime.now(datetime.UTC))
    updated_at = Column(
        sa.DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC),
        onupdate=datetime.datetime.now(datetime.UTC),
    )

    def __repr__(self):
        return f"Book(id={self.id}, title={self.title})"
