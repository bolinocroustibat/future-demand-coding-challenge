from datetime import datetime, timezone
from typing import Optional

from bs4 import BeautifulSoup

from crawlers.blueprint import EventsCrawler
from models.events import Event


class LucerneFestivalCrawler(EventsCrawler):

    # The host (used for relative URLs)
    HOST = "https://www.lucernefestival.ch"

    # The URLs to start with
    START_URLS = [
        # "https://www.lucernefestival.ch/en/tickets/program"
        "https://www.lucernefestival.ch/en/program/summer-festival-22",
    ]

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
        """
        Get the event info form an event page soup.
        Returns an instanciated Event object with the event info.
        """
        url_soup = soup.find("p", class_="event-title")
        url: str = self.HOST + url_soup.find("a").get("href")
        soup = self._get_soup_from_url(url=url)
        if soup:
            start_datetime: Optional[datetime] = None
            end_datetime: Optional[datetime] = None
            venue: Optional[str] = None
            artists_str: Optional[str] = None
            image_url: Optional[str] = None
            description: Optional[str] = None

            # Title
            title = soup.find("h1").text.strip()

            # Image URL
            image_soup = soup.find("figure", class_="fullscreen-image")
            image_url = (
                self.HOST + image_soup.find("img").get("src") if image_soup else None
            )

            # Description
            description_soup = soup.find("h2", text="Description")
            description = (
                description_soup.find_next_sibling("div").text.strip()
                if description_soup
                else None
            )

            # Artists
            artists_soup = soup.find("ul", class_="performers-list")
            if artists_soup:
                artists: list = [
                    li_soup.strong.text.strip()
                    for li_soup in artists_soup.find_all("li")
                ]
                artists_str = ", ".join(artists)

            # Date & Venue
            date_and_venue_soup = soup.find("strong", text="Date and Venue")
            if date_and_venue_soup:
                date_and_venue: list = (
                    date_and_venue_soup.next_sibling.next_sibling.text.split("|")
                )
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
            # # Another way to get the location
            # location_soup = soup.find("h2", text="Event Venue")
            # venue_name_soup = location_soup.find_next_sibling("div") if location_soup else None
            # location: str = venue_name_soup.find("p", class_="title").text.strip()

            if title and start_datetime:
                return Event(
                    source=self.HOST,
                    name=title,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                    location=venue,
                    artists=artists_str,
                    image_url=image_url,
                    description=description,
                    created=datetime.now(timezone.utc),
                )

        return None
