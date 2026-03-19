import tomllib
from collections.abc import Iterable
from pathlib import Path

from .types import Forms


def _read_project_version(pyproject_path: Path) -> str:
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    return data["project"]["version"]


def to_rime(
    out_dir: str,
    name: str,
    words: Iterable[str],
    pinyin: Iterable[str],
) -> None:
    version = _read_project_version(Path("pyproject.toml"))
    # fmt: off
    header = (
        "---\n"
        f"name: {name}\n"
        f'version: "{version}"\n'
        "sort: by_weight\n"
        "...\n"
    )
    # fmt: on

    path = Path(out_dir) / "cn_dicts"
    path.mkdir(parents=True, exist_ok=True)

    with (path / f"{name}.dict.yaml").open("w", encoding="utf-8", newline="\n") as f:
        f.write(header)
        f.writelines(f"{word}\t{py}\n" for word, py in zip(words, pinyin, strict=True) if word)


def to_opencc(
    out_dir: str,
    name: str,
    words_list: Iterable[Forms],
    mappings: Iterable[Forms],
) -> None:
    path = Path(out_dir) / "opencc"
    path.mkdir(parents=True, exist_ok=True)

    with (path / f"{name}.txt").open("w", encoding="utf-8", newline="\n") as f:
        for words, mapping in zip(words_list, mappings, strict=True):
            f.writelines(f"{word}\t{' '.join((word, *mapping))}\n" for word in words)
