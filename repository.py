from database import new_session
from models import Book
from schemas import SBookAdd
from sqlalchemy import insert, select, update, delete


class BookRepository:
    @staticmethod
    async def add_book(data: SBookAdd):
        async with new_session() as session:
            new_book = Book(
                name=data.name,
                author=data.author,
                year=data.year,
                publisher=data.publisher,
            )
            session.add(new_book)
            await session.flush()
            await session.commit()
            return new_book.id



if __name__ == "__main__":
    import asyncio

    book_ex = SBookAdd(
        name="How to threat arythmies",
        author="Nedostup A.V.",
        year=2014,
        publisher="Medpress",
    )

    res = asyncio.run(BookRepository.add_book(book_ex))
    print(res)