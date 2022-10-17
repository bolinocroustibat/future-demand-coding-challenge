import matplotlib.pyplot as plt
import pandas as pd
import psycopg2
import seaborn as sns
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

    logger.info("Eporting events table from database in CSV format...")

    sql: str = "COPY (SELECT * FROM events) TO STDOUT WITH CSV DELIMITER ','"

    connection = psycopg2.connect(POSTGRES_URL)
    cursor = connection.cursor()
    with open(CSV_PATH, "w") as file:
        cursor.copy_expert(sql, file)
    cursor.close()
    logger.success("Database exported to CSV.")


@app.command()
def plot() -> None:
    logger.info("Plotting the data with Seaborn...")
    df = pd.read_csv(
        CSV_PATH,
        names=["id", "name", "start_datetime", "end_datetime", "location", "artists"],
        header=None,
    )
    df = (
        pd.to_datetime(df["start_datetime"])
        .dt.floor("d")
        .value_counts()
        .rename_axis("Day")
        .reset_index(name="Events")
    )
    fig, ax = plt.subplots(figsize=(8, 8))
    fig = sns.barplot(x="Day", y="Events", data=df, order=df["Day"])
    x_dates = df["Day"].dt.strftime("%Y-%m-%d").sort_values().unique()
    ax.set_xticklabels(labels=x_dates, rotation=45, ha="right")
    plt.show()


@app.command()
def run(
    crawler_name: str = typer.Option(None, help="Name of the specific crawler."),
    verbose: bool = typer.Option(True, help="Verbose mode."),
) -> None:
    crawl(crawler_name=crawler_name, verbose=verbose)
    export_db()
    plot()


if __name__ == "__main__":
    app()
