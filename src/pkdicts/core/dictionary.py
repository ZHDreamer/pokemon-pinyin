import logging
from collections.abc import Generator
from dataclasses import dataclass, field
from itertools import chain, tee

from pkdicts.core.constant import PREFIX

from . import exporter
from .parse_page import PageParser, Selector
from .pinyin import PinyinGenerator
from .types import Forms

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@dataclass
class ScrapeConfig:
    name: str
    words: list[Selector]
    translates: list[Selector] = field(default_factory=list)


@dataclass
class Entry:
    word: Forms
    translation: Forms = field(default_factory=list)


class Dictionary:
    name: str
    output_directory: str

    words_selectors: list[Selector]
    translates_selectors: list[Selector]
    entries: list[Entry]

    def __init__(
        self,
        config: ScrapeConfig,
        output_directory: str,
        page_parser: PageParser,
        pinyin_generator: PinyinGenerator,
    ) -> None:
        self.name = config.name
        self.output_directory = output_directory

        self.words_selectors = config.words
        self.translates_selectors = config.translates

        self.entries = []
        self.parser = page_parser
        self.pinyin_generator = pinyin_generator

    def scrape(self) -> None:
        words_list = self.parser.parse(self.words_selectors)
        translations_list = self.parser.parse(self.translates_selectors)

        for forms_list in zip(*words_list, strict=True):
            word = list(dict.fromkeys(chain.from_iterable(forms_list)))
            entry = Entry(word=word)
            self.entries.append(entry)

        for entry, translations in zip(
            self.entries,
            zip(*translations_list, strict=True),
            strict=False,
        ):
            entry.translation = list(dict.fromkeys(chain.from_iterable(translations)))

        self._log_variants()

    def generate_dictionary(self) -> None:
        name = f"{PREFIX}_{self.name}"
        dictionary_entries, pinyins = tee(self._get_dictionary_entries())
        pinyins = self.pinyin_generator.get_pinyin(pinyins)
        exporter.to_rime(self.output_directory, name, dictionary_entries, pinyins)

    def generate_translation(self) -> None:
        if not self.translates_selectors:
            logger.info(
                "%s - No translation keys provided, skipping translation export.",
                self.name,
            )
            return

        exporter.to_opencc(
            self.output_directory,
            self.name,
            (entry.word for entry in self.entries),
            (entry.translation for entry in self.entries),
        )

    def _log_variants(
        self,
    ) -> None:
        for entry in self.entries:
            if len(entry.word) > 1:
                logger.info(
                    "%s - %s has variants: %s",
                    self.name,
                    entry.word[0],
                    entry.word[1:],
                )

    def _get_dictionary_entries(self) -> Generator[str]:
        return (form for entry in self.entries for form in entry.word)
