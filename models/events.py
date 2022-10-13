from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, UniqueConstraint, create_engine


class Event(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("name", "start_time"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    artists: Optional[str] = None


engine = create_engine("postgresql://postgres@localhost:5432/future-demand", echo=True)

SQLModel.metadata.create_all(engine)
