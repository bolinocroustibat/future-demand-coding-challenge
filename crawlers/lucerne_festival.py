from datetime import datetime
from typing import Optional

from bs4 import BeautifulSoup

from crawlers.blueprint import EventsCrawler
from models.events import Event


class LucerneFestivalCrawler(EventsCrawler):

    # The host (used for relative URLs)
    HOST = "https://www.lucernefestival.ch"

    # The URLs to start with
    START_URLS = [
        "https://www.lucernefestival.ch/en/tickets/program"
        # "https://www.lucernefestival.ch/en/program/summer-festival-22",
    ]

    # The urls that are allowed as articles
    ALLOWED_URLS = ["www.lucernefestival.ch"]

    # Events from lucernefestival.ch don't have a year, so it needs to be set manually
    YEAR = "2022"

    def _get_events(self, soup: BeautifulSoup) -> Optional[list[Event]]:
        events_list_soup = soup.find("ul", class_="event-list")
        if events_list_soup:
            if self.verbose:
                self.logger.success("Found events!")
            events: list = []
            for li_soup in events_list_soup.find_all("li"):
                event: Optional[Event] = self._get_event(soup=li_soup)
                if event:
                    events.append(event)
            # self.logger.debug(events)
            return events
        return None

    def _get_event(self, soup: BeautifulSoup) -> Optional[Event]:
        title = soup.find("p", class_="event-title").text.strip()
        start_datetime: Optional[datetime] = None
        end_datetime: Optional[datetime] = None
        artists_str: Optional[str] = None
        childs_soup = soup.find_all("div", class_="cell xlarge-6 body-small")
        if "Date and Venue" in childs_soup[0].text:
            # Date and Venue
            childs_soup[0].strong.extract()
            date_and_venue: list = childs_soup[0].text.split("|")
            date: str = date_and_venue[0].strip()
            time: str = date_and_venue[1].strip()
            if len(time.split("/")) > 1:
                times: list = time.split("/")
                start_datetime = datetime.strptime(
                    "{}{} {}".format(date, self.YEAR, times[0].strip()),
                    "%a %d.%m.%Y %H.%M",
                )
                end_datetime = datetime.strptime(
                    "{}{} {}".format(date, self.YEAR, times[1].strip()),
                    "%a %d.%m.%Y %H.%M",
                )
            else:
                start_datetime = datetime.strptime(
                    f"{date}{self.YEAR} {time}", "%a %d.%m.%Y %H.%M"
                )
                end_datetime = None
            venue: str = date_and_venue[2].strip()
        if "Program" in childs_soup[1].text:
            # Program
            childs_soup[1].strong.extract()
            artists: list = [a.strip() for a in childs_soup[1].text.split("|")]
            artists_str: str = ", ".join(artists)

        if title and start_datetime:
            return Event(
                name=title,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                location=venue,
                artists=artists_str,
            )

        return None
