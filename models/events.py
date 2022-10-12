from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    location: Optional[str] = None
    artists: Optional[str] = None


event_1 = Event(name="Funkdemic", location="Izu")

engine = create_engine("postgresql://postgres@localhost:5432/future-demand", echo=True)

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(event_1)
    session.commit()
