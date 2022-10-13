import psycopg2
import typer
from sqlmodel import SQLModel

from crawlers.lucerne_festival import LucerneFestivalCrawler
from helpers import CustomLogger
from settings import CSV_PATH, POSTGRES_URL, engine

app = typer.Typer()
logger = CustomLogger()


CRAWLERS: dict = {
    "lucernefestival": LucerneFestivalCrawler,
}


@app.command()
def create_table() -> None:
    SQLModel.metadata.create_all(engine)
    logger.success("Table created.")


@app.command()
def crawl(
    crawler_name: str = typer.Option(None, help="Name of the specific crawler."),
    verbose: bool = typer.Option(True, help="Verbose mode."),
) -> None:
    crawler_class = get_crawler_class(crawler_name)
    if not crawler_class:
        logger.error(f"Crawler {crawler_name} not found.")
    else:
        crawler = crawler_class(logger=logger, verbose=verbose)
        crawler.run()


def get_crawler_class(name: str):
    """
    Get the crawler class from the name, according to CRAWLERS dict.
    :returns: Crawler class
    """
    for key, value in CRAWLERS.items():
        if key == name:
            return value
    return None


@app.command()
def export_db() -> None:

    sql: str = "COPY (SELECT * FROM event) TO STDOUT WITH CSV DELIMITER ','"

    connection = psycopg2.connect(POSTGRES_URL)
    cursor = connection.cursor()
    with open(CSV_PATH, "w") as file:
        cursor.copy_expert(sql, file)
    cursor.close()
    logger.success("Database exported to CSV.")


if __name__ == "__main__":
    app()
