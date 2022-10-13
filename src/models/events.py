from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, UniqueConstraint


class Event(SQLModel, table=True):
    __tablename__ = 'events'
    __table_args__ = (UniqueConstraint("name", "start_datetime"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    start_datetime: datetime
    end_datetime: Optional[datetime] = None
    location: Optional[str] = None
    artists: Optional[str] = None
