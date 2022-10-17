from typing import Optional

from sqlmodel import Field, SQLModel, UniqueConstraint


class Location(SQLModel, table=True):
    __tablename__ = "locations"
    __table_args__ = (UniqueConstraint("name"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
