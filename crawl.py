import typer

from helpers import CustomLogger
from settings import CRAWLERS

app = typer.Typer()
logger = CustomLogger()


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
    Get the crawler class from the name, according to CRAWLERS dict in settings.py.
    :returns: Crawler class
    """
    for key, value in CRAWLERS.items():
        if key == name:
            return value
    return None


if __name__ == "__main__":
    typer.run(crawl)
