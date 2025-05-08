from typing import Annotated
from sqlalchemy import delete
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database import engine, new_session


class BaseModel(DeclarativeBase):
    pass

class Book(BaseModel):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Annotated[str, 256]]
    author: Mapped[Annotated[str, 256]]
    year: Mapped[int]
    publisher: Mapped[Annotated[str, 10]]

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

async def clear_books_table():
    async with new_session() as session:
        query = delete(Book)
        await session.execute(query)
        await session.commit()


if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(clear_books_table())
    except Exception as e:
        print(f"Error has been occurred: {type(e)}:, {e}")