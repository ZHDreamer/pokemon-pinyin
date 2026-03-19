from collections.abc import Sequence
from pathlib import Path

import click
import json5

from .configs import CONFIGS
from .core.dictionary import Dictionary
from .core.parse_page import PageParser
from .core.pinyin import PinyinGenerator

DATA_DIR = "data"
FIX_FILE = "fixfile.json5"
DEFAULT_OUTPUT_DIR = "dist"
DEFAULT_CONFIG_NAME = "pokemon"


available_configs = ", ".join(CONFIGS.keys())


def run_config(
    config_names: Sequence[str] = (DEFAULT_CONFIG_NAME,),
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> None:
    """Run one or more configurations."""
    pinyin_generator = PinyinGenerator()
    pinyin_generator.pinyin_replace = {
        "Ⅱ": "2",
    }
    with (Path(DATA_DIR) / FIX_FILE).open("r", encoding="utf-8") as f:
        pinyin_generator.load_phrases_dict(json5.load(f))

    for config_name in config_names:
        if config_name not in CONFIGS:
            msg = f"Config '{config_name}' not found. Available configs: {available_configs}"
            raise ValueError(msg)

        config = CONFIGS[config_name]

        dictionary = Dictionary(
            config,
            output_dir,
            page_parser=PageParser(),
            pinyin_generator=pinyin_generator,
        )
        dictionary.scrape()
        dictionary.generate_dictionary()
        dictionary.generate_translation()


@click.command()
@click.argument("config_names", nargs=-1)
@click.option("--output-dir", default=DEFAULT_OUTPUT_DIR, show_default=True)
@click.option("--all", "build_all", is_flag=True, help="Build all available configs.")
def cli(config_names: tuple[str, ...], output_dir: str, *, build_all: bool) -> None:
    """Generate dictionaries for a selected config."""
    if build_all:
        run_config(config_names=tuple(CONFIGS), output_dir=output_dir)
        return

    if not config_names:
        msg = (
            "No config names provided. ",
            f"Use --all to build all configs or specify config names: {available_configs}",
        )
        raise ValueError(msg)

    run_config(config_names=config_names, output_dir=output_dir)


if __name__ == "__main__":
    cli()
