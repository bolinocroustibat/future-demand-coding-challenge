# Future Demand Coding Challenge

## Main dependencies

- Python 3.9+
- Docker

### Main Python packages

This project use the following Python packages:
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [psycopg2](https://pypi.org/project/psycopg2-binary/), a Python PostgreSQL driver. We use the binary version here in case PostgreSQL is not already installed.
- [SQLmodel](https://sqlmodel.tiangolo.com/), an async Python ORM made by the creator of beloved [FastAPI](https://fastapi.tiangolo.com/)
- [Typer](https://typer.tiangolo.com/)
- [TQDM](https://github.com/tqdm/tqdm)

## Pre-requisites

- Install Docker, if not already

- Start Docker

- Export env variable `POSTGRES_DB` for defining the name of your PostgreSQL database:
```sh
export POSTGRES_DB="future-demand"
```

- Start Docker compose:
```ssh
docker-compose up -d
```

- Install Python dependencies:
```sh
pip install -r requirements.txt
```
...or, if you have [Poetry](https://python-poetry.org/) installed:
```sh
poetry install
```
...or:
```sh
make install
```

## Crawlers configuration

Each crawler, for each website, can have specific parameters.
The configuration can be done in each crawler class file, in the `crawler` folder, for example in `crawlers/lucerne_festival.py` file.
Minimum crawlers parameters are:
- `HOST`: the base URL of the website,
- `START_URLS`: the URL of the pages to start crawling from.

Each crawler can have more specific parameters, depending on the website.

## Commands

- To create the database table:
```sh
python3 main.py create-db [--help]
```

- To run a crawler:
```sh
python3 main.py crawl [--crawler-name] [--help] [--verbose]
```
for example:
```sh
python3 main.py crawl "lucernefestival"
```

- To export the DB to a CSV file:
```sh
python3 main.py export-db [--help]
```

## Possible future improvements

- Add unit tests, using [pytest](https://docs.pytest.org/en/stable/).
- Use a separate table for artists and events, with a many-to-many relationship between them.
- Add more crawlers for other websites. The current architecture is flexible enough to add more crawlers very easily.
- Save the locations as a separate table, with a many-to-many relationship with the events.
- Save the locations as GeoJSON, to be able to use the [PostGIS](https://postgis.net/) extension of PostgreSQL.
- Manage the update of an existing event, if it is re-parsed.
- Use FastAPI and Uvicorn to create a small website and webserver to serve the plots as a webpage.
