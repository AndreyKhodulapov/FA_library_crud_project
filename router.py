from fastapi import APIRouter


router = APIRouter(
    prefix="/books",
    tags=["BOOK CRUD"],
)

@router.get("")
async def get_all_books():
    ...

@router.get("")
async def get_filtered_books():
    ...

@router.get("/{book_id}")
async def get_one_book_by_name(book_id: int):
    ...

@router.post("")
async def add_new_book():
    ...

@router.put("/{book_id}")
async def update_book_by_id():
    ...

@router.patch("/{book_id}")
async def partly_update_book_by_id():
    ...

@router.delete("/{book_id}")
async def delete_book_by_id():
    ...