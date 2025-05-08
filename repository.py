from database import new_session
from models import Book
from schemas import SBookAdd, SBookGet, SBookFilter
from sqlalchemy import select, update, delete


class BookRepository:
    @classmethod
    async def add_book(cls, data: SBookAdd) -> int:
        async with new_session() as session:
            data_dict = data.model_dump()  # convert to dict
            new_book = Book(**data_dict)  # model get params as dict
            session.add(new_book)
            await session.flush()
            await session.commit()
            return new_book.id

    @classmethod
    async def get_all_books(cls) -> list[SBookGet]:
        async with new_session() as session:
            query = select(Book)
            result = await session.execute(query)
            book_models = result.scalars().all()
            book_schemas = [
                SBookGet.model_validate(model)
                for model in book_models
            ]
            return book_schemas

    @classmethod
    async def get_book_by_id(cls, book_id: int) -> SBookGet | None:
        async with new_session() as session:
            query = select(Book).filter(Book.id == book_id)
            result = await session.execute(query)
            try:
                book_model = next(result)
            except StopIteration:
                return None
            book_schema = SBookGet.model_validate(book_model[0])
            return book_schema

    @classmethod
    async def delete_book_by_id(cls, book_id: int) -> str:
        async with new_session() as session:
            book = await cls.get_book_by_id(book_id)
            if not book:
                return f"There is no book with {book_id=}"
            stmt = delete(Book).filter(Book.id == book_id)
            await session.execute(stmt)
            await session.commit()
            return f"Book with {book_id=} has been successfully deleted!"

    @classmethod
    async def update_book_info(cls,
                               book_id: int,
                               update_data: SBookAdd):
        async with new_session() as session:
            book = await cls.get_book_by_id(book_id)
            if not book:
                return f"There is no book with {book_id=}"
            stmt = (update(Book)
                    .where(Book.id == book_id)
                    .values(**update_data.model_dump()))
            await session.execute(stmt)
            await session.commit()
            return f"Successfully updated: {book_id=} {book} ==> {update_data}"

    @classmethod
    async def partly_update_book_info(cls,
                               book_id: int,
                               update_data: SBookFilter):
        async with new_session() as session:
            book = await cls.get_book_by_id(book_id)
            if not book:
                return f"There is no book with {book_id=}"
            # stmt = (update(Book)
            #         .where(Book.id == book_id)
            #         .values(**update_data.model_dump()))
            await session.execute(stmt)
            await session.commit()
            return f"Successfully updated: {book_id=}: {update_data}"

#finish partly
#check func
#see by filters
#hanlders









if __name__ == "__main__":
    import asyncio

    book_ex = SBookAdd(
        name="Arrhithmia treatment",
        author="Nedostup A.V.",
        year=2014,
        publisher="Medpress",
    )

    book_new = SBookAdd(
        name="Heart troponines",
        author="Krikunova O.V.",
        year=2016,
        publisher="MedInfo",
    )

    # res = asyncio.run(BookRepository.add_book(book_ex))
    # res = asyncio.run(BookRepository.get_all_books())
    # res = asyncio.run(BookRepository.get_book_by_id(2))
    # res = asyncio.run(BookRepository.get_book_by_id(20))
    # res = asyncio.run(BookRepository.delete_book_by_id(3))
    # res = SBookFilter()
    res = asyncio.run(BookRepository.update_book_info(3, book_new))
    print(res)