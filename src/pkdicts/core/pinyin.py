from collections.abc import Generator, Iterable

from pypinyin import Style, lazy_pinyin, load_phrases_dict, load_single_dict


class PinyinGenerator:
    """Handles pinyin generation with custom dictionaries and replacements."""

    def __init__(
        self,
        pinyin_dict: dict[str, str] | None = None,
        phrases_dict: dict[str, str] | None = None,
        pinyin_replace: dict[str, str] | None = None,
    ) -> None:
        self.pinyin_replace = pinyin_replace or {}
        if pinyin_dict:
            self.load_single_dict(pinyin_dict)
        if phrases_dict:
            self.load_phrases_dict(phrases_dict)

    def load_single_dict(self, pinyin_dict: dict[str, str]) -> None:
        """Load custom single character pinyin dictionary."""
        load_single_dict({ord(k): v for k, v in pinyin_dict.items()})

    def load_phrases_dict(self, phrases_dict: dict[str, str]) -> None:
        """Load custom phrases pinyin dictionary."""
        phrases = {}
        for phrase, pinyin in phrases_dict.items():
            pinyin_list = [[p.strip()] for p in pinyin.split()]
            phrases[phrase] = pinyin_list

        load_phrases_dict(phrases)

    def get_pinyin(self, words: Iterable[str]) -> Generator[str]:
        """Generate pinyin for the given words."""
        for word in words:
            pinyin_list = lazy_pinyin(
                word,
                style=Style.NORMAL,
                errors=lambda x: " ".join(c.upper() if c.isalpha() else c for c in x),
            )
            pinyin_list = [self.pinyin_replace.get(x, x) for x in pinyin_list]
            pinyin = " ".join(pinyin_list)
            yield pinyin
