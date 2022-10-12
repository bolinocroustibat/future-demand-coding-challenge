import re
from datetime import datetime
from typing import Generator, Iterator, List, Match, Optional, Set

import requests
from bs4 import BeautifulSoup


class ArticlesCrawler:

    HEADERS: str = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }

    def __init__(
        self,
        logger,
        verbose: bool,
    ) -> None:
        self.logger = logger
        self.verbose = verbose

    def run(self, urls: Optional[List[str]] = None) -> Generator:
        """
        :returns: a generator of dicts with the following structure:
        """
        if self.verbose:
            self.logger.info(f"Getting links from {self.START_URLS}...")
        if urls:
            for url in urls:
                if not self.datafile.if_entry_exists(url=url) or self.update:
                    if self.verbose:
                        self.logger.info(f"Parsing content from {url}...")
                    yield self._build_response(url=url)
        else:
            if self.START_URLS:
                for url in self.START_URLS:
                    if self.verbose:
                        self.logger.info(f"Getting links from {url}...")
                    for link in self._extract_links(url=url):
                        if link != url:
                            if (
                                not self.datafile.if_entry_exists(url=url)
                                or self.update
                            ):
                                if self.verbose:
                                    self.logger.info(
                                        f"Found page {link}. Parsing content..."
                                    )
                                # Go through all the found links
                                yield self._get_events_from_page(url=link)
            self.logger.error(
                f"No URLs to parse found for crawler {self.__class__.__name__}"
            )

    def _extract_links(self, url: str) -> Set:
        """
        Extract all links from a given URL.
        :returns: set of unique urls (str)
        """
        html = requests.get(url, headers=self.HEADERS).content
        soup = BeautifulSoup(html, "html.parser")
        links_soup = soup.findAll(
            "a", href=re.compile(r"\b(?:{})\b".format("|".join(self.ALLOWED_URLS)))
        )  # https://stackoverflow.com/questions/6750240/how-to-do-re-compile-with-a-list-in-python
        # self.logger.debug(str(links_soup))
        return set(l["href"] for l in links_soup)

    def _get_events_from_page(self, url: str) -> Optional[dict]:
        soup = self._get_soup(url=url)
        if soup:
            content = self._get_content(soup=soup)
            if content:
                # TODO use Event SQLmodel class
                return {
                    "url": url,
                    "title": self._get_title(soup=soup),
                    "eventLocation": self._get_location(soup=soup),
                    "eventDate": self._get_published_time(soup=soup),
                    "eventTime": self._get_modified_time(soup=soup),
                    "artists": None,
                    "dateParsed": datetime.utcnow().strftime("%Y-%m-%d_%H-%M"),
                }
        return None

    def _get_soup(self, url: str) -> Optional[BeautifulSoup]:
        try:
            html = requests.get(url, headers=self.HEADERS).content
        except Exception as e:
            self.logger.error(f"Request error: {str(e)}")
        else:
            return BeautifulSoup(html, "html.parser")
        return None
