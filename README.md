# Future Demand Coding Challenge


## Main Python dependencies

- Python 3.9+
- Docker

### Python packages

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Typer](https://typer.tiangolo.com/)
- [TQDM](https://github.com/tqdm/tqdm)

## How to run

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

- Run the script
```sh
python3 crawl.py [--help] [--verbose]
```
