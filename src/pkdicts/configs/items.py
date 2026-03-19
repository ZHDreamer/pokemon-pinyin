from pkdicts.core import processor
from pkdicts.core.dictionary import ScrapeConfig
from pkdicts.core.parse_page import Selector

page = "道具列表"

selectors = [
    "td:nth-child(-n+2)>a",
]

config = ScrapeConfig(
    name="items",
    words=[
        Selector(
            variant="zh-hans",
            page=page,
            element=selectors[0],
            processor=processor.compose(
                processor.NFKC,
                processor.fork(
                    processor.replace_keywords(
                        {
                            "咒术": "诅咒",
                            "谜拟丘": "谜拟Q",
                        },
                    ),
                    processor.noop,
                    processor.remove_suffix_by_keywords(
                        [
                            "XS",
                            "S",
                            "M",
                            "L",
                            "XL",
                            "X",
                            "Y",
                            r"\d{1,2}",
                        ],
                    ),
                ),
                processor.remove_repeat,
                processor.remove_single_char,
            ),
        ),
    ],
)
