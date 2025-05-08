from fastapi import APIRouter


router = APIRouter(
    prefix="/books",
    tags=["BOOK CRUD"],
)

