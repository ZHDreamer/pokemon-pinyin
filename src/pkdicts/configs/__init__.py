import os
from importlib import import_module
from pathlib import Path

from pkdicts.core.dictionary import ScrapeConfig


def _load_config() -> dict[str, ScrapeConfig]:
    result = {}

    for config in os.scandir(Path(__file__).parent):
        if config.name.endswith(".py") and not config.name.startswith("_"):
            module_name = config.name[:-3]
            module = import_module(f".{module_name}", __package__)
            result[module.config.name] = module.config

    return result


CONFIGS = _load_config()

__all__ = ["CONFIGS"]
