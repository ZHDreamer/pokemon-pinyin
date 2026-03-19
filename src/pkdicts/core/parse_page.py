import logging
from collections.abc import Callable, Generator, Iterable
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag

from .constant import BASE_URL, REQUEST_TIMEOUT, USER_AGENT
from .processor import noop
from .types import Forms, Processor


@dataclass
class Selector:
    variant: str
    page: str
    element: str
    processor: Processor = noop
    extractor: Callable[[Tag], list[str]] = lambda element: [element.get_text(strip=True)]


logger = logging.getLogger(__name__)


class PageParser:
    """Handles page fetching and parsing with built-in caching."""

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    def __init__(self) -> None:
        self._cache: dict[str, BeautifulSoup] = {}

    def parse(self, selectors: Iterable[Selector]) -> Generator[Generator[Forms]]:
        """Parse multiple selectors, caching pages by URL."""
        for selector in selectors:
            soup = self._fetch_page_content(
                BASE_URL,
                params={
                    "action": "parse",
                    "variant": selector.variant,
                    "page": selector.page,
                    "format": "json",
                    "formatversion": "2",
                    "utf8": "1",
                },
            )
            if not soup:
                continue
            elements = soup.select(selector.element)
            if not elements:
                logger.warning(
                    "No elements found for selector of URL %s",
                    selector.page,
                )
                continue
            elements = ([item] for element in elements for item in selector.extractor(element))
            elements = selector.processor(elements)
            yield elements

    def _fetch_page_content(self, url: str, params: dict[str, str]) -> BeautifulSoup:
        if url in self._cache:
            return self._cache[url]

        try:
            respond = self.session.get(url, params=params, timeout=REQUEST_TIMEOUT)
            respond.raise_for_status()
            data = respond.json()
            soup = BeautifulSoup(data["parse"]["text"], "html.parser")
        except requests.exceptions.Timeout:
            logger.exception("Request timed out after %s seconds.", REQUEST_TIMEOUT)
        except requests.exceptions.RequestException:
            logger.exception("Error fetching the page")

        self._cache[url] = soup
        return soup
