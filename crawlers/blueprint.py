import re
from typing import Optional, Set

import requests
from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from tqdm import tqdm

from models.events import Event
from settings import engine


class EventsCrawler:

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }

    def __init__(
        self,
        logger,
        verbose: bool,
    ) -> None:
        self.logger = logger
        self.verbose = verbose

    def run(self) -> None:
        """
        :returns: a generator of Event objects
        """
        if self.START_URLS:
            self.logger.info(f"Parsing pages of website {self.__class__.HOST}...")
            for url in self.START_URLS:
                if self.verbose:
                    self.logger.info(f"Parsing content from {url}...")
                # Parse the page for events
                events: Optional[list[Event]] = self._get_events_from_page(url=url)
                if events:
                    self._save_into_database(events=events)
                if self.verbose:
                    self.logger.info(f"Getting links from {url}...")
                for link in tqdm(self._extract_links(url=url)):
                    if link != url:
                        if self.verbose:
                            self.logger.info(f"Found page {link}. Parsing content...")
                        # Parse the page for events
                        events = self._get_events_from_page(url=link)
                        if events:
                            self._save_into_database(events=events)
            self.logger.warning(
                f"No more URLs to parse found for crawler {self.__class__.__name__}."
            )

    def _extract_links(self, url: str) -> Set[str]:
        """
        Extract all links from a given URL.
        :returns: set of unique urls
        """

        html = requests.get(url, headers=self.HEADERS).content
        soup = BeautifulSoup(html, "html.parser")
        links = set()

        # Find all absolute links that match with the crawler HOST
        absolute_links_soup = soup.find_all(
            "a", href=re.compile(r"\b(?:{})\b".format(self.HOST))
        )
        # If we want to allow several hosts
        # absolute_links_soup = soup.find_all(
        #     "a", href=re.compile(r"\b(?:{})\b".format("|".join([self.ALLOWED_HOSTS])))
        # ) # https://stackoverflow.com/questions/6750240/how-to-do-re-compile-with-a-list-in-python
        for link in absolute_links_soup:
            self.logger.debug(f"Found absolute link {link['href']}")
            link.add(link["href"])

        # Find all relative links and add the domain
        relative_links_soup = soup.find_all("a", href=re.compile(r"^/"))
        for link in relative_links_soup:
            links.add(f"{self.HOST}{link['href']}")

        # self.logger.debug(links)

        return links

    def _get_events_from_page(self, url: str) -> Optional[list[Event]]:
        try:
            html = requests.get(url, headers=self.HEADERS).content
        except Exception as e:
            self.logger.error(f"Request error: {str(e)}")
        else:
            soup = BeautifulSoup(html, "html.parser")
            if soup:
                return self._get_events(soup=soup)
            return None

    def _save_into_database(self, events: list[Event]) -> None:
        """
        Save alist of Event objects into the database.
        """
        for event in events:
            with Session(engine) as session:
                try:
                    session.add(event)
                    session.commit()
                except IntegrityError as e:
                    self.logger.warning(
                        f'Couldn\'t save event "{event.name}" into the database, probably because it already exists.'
                    )
                except Exception as e:
                    self.logger.error(
                        f'Couldn\'t save event "{event.name}" into the database: {str(e)}'
                    )
                else:
                    self.logger.success(
                        f'Saved event "{event.name}" into the database.'
                    )
