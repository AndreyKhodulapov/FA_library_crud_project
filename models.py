from typing import Annotated
from fastapi import APIRouter
from sqlalchemy import delete, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database import engine, new_session
from schemas import MyResponse


class BaseModel(DeclarativeBase):
    pass

class Book(BaseModel):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Annotated[str, 256]]
    author: Mapped[Annotated[str, 256]]
    year: Mapped[int]
    publisher: Mapped[Annotated[str, 10]]

admin_router = APIRouter(
    prefix="/admin",
    tags=["Table management"]
)

@admin_router.get("")
async def show_tables():
    async with engine.connect() as conn:
        tables = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
            )
        return MyResponse(
            ok=True,
            message=f"Created tables are: {tables}"
        )

@admin_router.post("")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

@admin_router.delete("")
async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

@admin_router.patch("")
async def clear_books_table():
    async with new_session() as session:
        query = delete(Book)
        await session.execute(query)
        await session.commit()

