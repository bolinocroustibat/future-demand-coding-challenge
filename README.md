# Future Demand Coding Challenge

## Main Python dependencies

- Python 3.9+
- Docker

### Main Python packages

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [psycopg2](https://pypi.org/project/psycopg2-binary/), a Python PostgreSQL driver. We use the binary version here in case PostgreSQL is not already installed.
- [Typer](https://typer.tiangolo.com/)
- [SQLmodel](https://sqlmodel.tiangolo.com/), an async Python ORM made by the creator of beloved [FastAPI](https://fastapi.tiangolo.com/)
- [TQDM](https://github.com/tqdm/tqdm)

## Requirements

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

## Commands

- Create the database table
```sh
python3 create_database.py [--help]
```

- Run the script
```sh
python3 crawl.py [--help] [--verbose]
```
