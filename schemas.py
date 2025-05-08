import datetime

from pydantic import BaseModel, Field, ConfigDict


class SBookAdd(BaseModel):
    name: str = Field(max_length=256)
    author: str = Field(max_length=256)
    year: int = Field(gt=1800, le=datetime.datetime.now().year)
    publisher: str = Field(max_length=10)

    model_config = ConfigDict(from_attributes=True)


class SBookGet(SBookAdd):
    id: int


class SBookFilter(SBookAdd):
    name: str | None = Field(max_length=256, default=None)
    author: str | None = Field(max_length=256, default=None)
    year: int | None = Field(gt=1800, le=datetime.datetime.now().year, default=None)
    publisher: str | None = Field(max_length=10, default=None)