from datetime import datetime

from sqlmodel import Field, SQLModel


class CityQueryBase(SQLModel):
    csrftoken: str = Field(max_length=100, nullable=True)
    timestamp: datetime | None = Field(default=datetime.now(), nullable=False)
    city: str = Field(max_length=30)


class CityQuery(CityQueryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class CityQueryCreate(CityQueryBase):
    pass


class CityStats(SQLModel):
    city: str
    count: int


class CityStatsRead(SQLModel):
    stats: list[CityStats]