import os
from sqlmodel import create_engine


POSTGRES_URL: str = f"postgresql://postgres@localhost:5432/{os.environ['POSTGRES_DB']}"

CSV_PATH = "data/events.csv"

engine = create_engine(POSTGRES_URL, echo=False)
