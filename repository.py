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
                if model is not None
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
    async def check_id(cls, identifier: int) -> bool:
        book = await cls.get_book_by_id(identifier)
        if not book:
            return False
        return True

    @classmethod
    async def get_by_filter(cls,
                            filter_data: SBookFilter) -> list[SBookGet] | None:
        async with new_session() as session:
            filters = []
            if filter_data.name is not None:
                filters.append(Book.name == filter_data.name)
            if filter_data.author is not None:
                filters.append(Book.author == filter_data.author)
            if filter_data.year is not None:
                filters.append(Book.year == filter_data.year)
            if filter_data.publisher is not None:
                filters.append(Book.publisher == filter_data.publisher)
            query = (select(Book)
                    .filter(*filters))
            result = await session.execute(query)
            book_models = result.scalars().all()
            book_schemas = [
                SBookGet.model_validate(model)
                for model in book_models
                if model is not None
            ]
            return book_schemas

    @classmethod
    async def delete_book_by_id(cls, book_id: int) -> str | None:
        async with new_session() as session:
            if not await cls.check_id(book_id):
                return None
            stmt = delete(Book).filter(Book.id == book_id)
            await session.execute(stmt)
            await session.commit()
            return f"Book with {book_id=} has been successfully deleted!"

    @classmethod
    async def update_book_info(cls,
                               book_id: int,
                               update_data: SBookAdd) -> str | None:
        async with new_session() as session:
            if not await cls.check_id(book_id):
                return None
            stmt = (update(Book)
                    .filter(Book.id == book_id)
                    .values(**update_data.model_dump()))
            await session.execute(stmt)
            await session.commit()
            return f"Successfully updated: {book_id=} ==> {update_data}"

    @classmethod
    async def partly_update_book_info(cls,
                               book_id: int,
                               update_data: SBookFilter) -> str | None:
        async with new_session() as session:
            if not await cls.check_id(book_id):
                return None
            update_values = {key: value
                             for key, value in update_data.model_dump().items()
                             if value is not None}
            stmt = (update(Book)
                    .filter(Book.id == book_id)
                    .values(**update_values))
            await session.execute(stmt)
            await session.commit()
            return f"Successfully updated: {book_id=}: {update_values}"

