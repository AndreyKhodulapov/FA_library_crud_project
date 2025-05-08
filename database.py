import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


load_dotenv()

db_url = os.getenv("DB_NAME")

engine = create_async_engine(db_url)

new_session = async_sessionmaker(
    engine=engine,
    expire_on_commit=False,
)

