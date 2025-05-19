from typing import Any

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession


class BookService:
    @staticmethod
    async def get_similar(
        book_id: int, limit: int, offset: int, *, session: AsyncSession
    ) -> list[dict[str, Any]]:
        query = sqlalchemy.text("""
WITH target_book_embedding AS (
    SELECT
        embedding AS reference_embedding
    FROM
        book
    WHERE
        id = :book_id
)

SELECT
    main_book.id                     AS id,
    main_book.title                  AS title,
    main_book.author                 AS author,
    main_book.genres                 AS genres,
    main_book.pages                  AS pages,
    main_book.year                   AS publication_year,
    1 - (main_book.embedding <=> target_book_embedding.reference_embedding) AS similarity
FROM
    book AS main_book

CROSS JOIN
    target_book_embedding
WHERE main_book.id != :book_id
ORDER BY
    similarity DESC
LIMIT :limit
OFFSET :offset
;
""")
        result = await session.execute(
            query,
            {
                "book_id": book_id,
                "limit": limit,
                "offset": offset,
            },
        )
        return [row._asdict() for row in result]
