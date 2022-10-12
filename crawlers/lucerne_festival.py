from typing import List, Optional

from bs4 import BeautifulSoup

from .blueprint import ArticlesCrawler


class LucerneFestivalCrawler(ArticlesCrawler):

    # The URLs to start with
    START_URLS = [
        "https://www.lucernefestival.ch/en/program/summer-festival-22",
    ]