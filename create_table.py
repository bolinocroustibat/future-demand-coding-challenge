import typer
from sqlmodel import SQLModel

from helpers import CustomLogger
from models.events import engine

app = typer.Typer()
logger = CustomLogger()


@app.command()
def create_table() -> None:
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    typer.run(create_table)
