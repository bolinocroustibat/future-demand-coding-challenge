from typing import Optional

from sqlmodel import Field, SQLModel, UniqueConstraint


class Artist(SQLModel, table=True):
    __tablename__ = "artists"
    __table_args__ = (UniqueConstraint("name"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
