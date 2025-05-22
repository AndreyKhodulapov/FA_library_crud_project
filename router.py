from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from repository import BookRepository
from schemas import SBookAdd, SBookFilter, SBookGet, MyResponse


router = APIRouter(
    prefix="/books",
    tags=["BOOK CRUD"],
)

@router.get("")
async def get_filtered_books(
        book: Annotated[SBookFilter, Depends()]
    ) -> MyResponse | list[SBookGet]:
    result = await BookRepository.get_by_filter(book)
    if not result:
        return MyResponse(
            ok=True,
            message=f"Books are not found!",
        )
    return result

@router.get("/{book_id}")
async def get_one_book_by_id(book_id: int) -> SBookGet:
    result = await BookRepository.get_book_by_id(book_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Book with {book_id=} was not found"
        )
    return result

@router.post("")
async def add_new_book(book: Annotated[SBookAdd, Depends()]) -> MyResponse:
    try:
        result = await BookRepository.add_book(book)
        return MyResponse(
            ok=True,
            message=f"Book {book.name} has been successfully added with id={result}",
        )
    except Exception:
        return MyResponse(
            ok=False,
            message="SOMETHING WENT WRONG, TRY LATER",
        )

@router.put("/{book_id}")
async def update_book_by_id(
        book_id: int,
        book: Annotated[SBookAdd, Depends()]
    ) -> MyResponse:
    result = await BookRepository.update_book_info(book_id, book)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Book with {book_id=} was not found"
        )
    return MyResponse(
        ok=True,
        message=result,
    )

@router.patch("/{book_id}")
async def partly_update_book_by_id(book_id: int,
        book: Annotated[SBookFilter, Depends()]
    ) -> MyResponse:
    result = await BookRepository.partly_update_book_info(book_id, book)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Book with {book_id=} was not found"
        )
    return MyResponse(
        ok=True,
        message=result,
    )


@router.delete("/{book_id}")
async def delete_book_by_id(book_id: int) -> MyResponse:
    result = await BookRepository.delete_book_by_id(book_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Book with {book_id=} was not found"
        )
    return MyResponse(
        ok=True,
        message=result,
    )