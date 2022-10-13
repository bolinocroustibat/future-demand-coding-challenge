import os
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, UniqueConstraint, create_engine


engine = create_engine(
    f"postgresql://postgres@localhost:5432/{os.environ['POSTGRES_DB']}",
    echo=False,
)


class Event(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("name", "start_datetime"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    start_datetime: datetime
    end_datetime: Optional[datetime] = None
    location: Optional[str] = None
    artists: Optional[str] = None