import asyncio
from schemas import *
from models import Book


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

p_update = SBookFilter(
        name="Clear code",
        author="Martin",
        year=2022,
    )

p_filter_1 = SBookFilter(
        publisher="MedInfo",
    )

p_filter_2 = SBookFilter(
        author="Pushkin",
    )

# res = asyncio.run(BookRepository.add_book(book_ex))
# res = asyncio.run(BookRepository.get_all_books())
# res = asyncio.run(BookRepository.get_book_by_id(2))
# res = asyncio.run(BookRepository.get_book_by_id(20))
# res = asyncio.run(BookRepository.delete_book_by_id(10))
# res = SBookFilter()
# res = asyncio.run(BookRepository.update_book_info(3, book_new))
# res = asyncio.run(BookRepository.partly_update_book_info(9, p_update))
# res = asyncio.run(BookRepository.get_by_filter(p_filter_2))
# print(res)