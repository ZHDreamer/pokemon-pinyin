import re
import unicodedata
from collections.abc import Generator, Iterable
from itertools import chain, tee

from opencc import OpenCC

from .types import Forms, Processor


def compose(*processors: Processor) -> Processor:
    def composed_processor(words: Iterable[Forms]) -> Generator[Forms]:
        for processor in processors:
            words = processor(words)
        yield from words

    return composed_processor


def fork(*branches: Processor) -> Processor:
    def forked_processor(words: Iterable[Forms]) -> Generator[Forms]:
        streams = tee(words, len(branches))
        branches_results = [
            branch(stream) for branch, stream in zip(branches, streams, strict=True)
        ]

        for forms_list in zip(*branches_results, strict=True):
            yield list(dict.fromkeys(chain.from_iterable(forms_list)))

    return forked_processor


def noop(words: Iterable[Forms]) -> Generator[Forms]:
    yield from words


def remove_characters(
    characters: Iterable[str],
) -> Processor:
    mapping = {ord(char): None for char in characters}
    return lambda words: ([form.translate(mapping) for form in forms] for forms in words)


def replace_characters(
    replacements: dict[str, str],
) -> Processor:
    mapping = {ord(char): replacement for char, replacement in replacements.items()}
    return lambda words: ([form.translate(mapping) for form in forms] for forms in words)


def replace_keywords(
    replacements: dict[str, str],
) -> Processor:
    pattern = "|".join(re.escape(k) for k in replacements)
    return lambda words: (
        [
            re.sub(
                pattern,
                lambda m: replacements[m.group(0)],
                form,
            )
            for form in forms
        ]
        for forms in words
    )


def remove_repeat(entries: Iterable[Forms]) -> Generator[Forms]:
    seen = set()
    for entry in entries:
        forms = []
        for form in entry:
            if form not in seen:
                forms.append(form)
                seen.add(form)

        yield forms


def remove_token(
    tokens: Iterable[str],
) -> Processor:
    tokens = set(tokens)
    return lambda words: ([form for form in forms if form not in tokens] for forms in words)


def remove_prefix_by_keywords(
    keywords: Iterable[str],
) -> Processor:
    pattern = r"^(?:{})".format("|".join(keywords))
    return lambda words: (
        [
            re.sub(
                pattern,
                "",
                form,
            )
            for form in forms
        ]
        for forms in words
    )


def remove_suffix_by_keywords(
    keywords: Iterable[str],
) -> Processor:
    pattern = r"(?:{})$".format("|".join(keywords))
    return lambda words: (
        [
            re.sub(
                pattern,
                "",
                form,
            )
            for form in forms
        ]
        for forms in words
    )


def remove_single_char(
    words: Iterable[Forms],
) -> Generator[Forms]:
    return ([form for form in forms if len(form) > 1] for forms in words)


def fw_latin_to_hw(words: Iterable[Forms]) -> Generator[Forms]:
    return (
        [
            re.sub(
                r"[！-～]",  # noqa: RUF001
                lambda m: chr(ord(m.group(0)) - 0xFEE0),
                form,
            )
            for form in forms
        ]
        for forms in words
    )


def NFKC(words: Iterable[Forms]) -> Generator[Forms]:  # noqa: N802
    return ([unicodedata.normalize("NFKC", form) for form in forms] for forms in words)


_converter = OpenCC("t2s")


def opencc_t2s(words: Iterable[Forms]) -> Generator[Forms]:
    return ([_converter.convert(form) for form in forms] for forms in words)
