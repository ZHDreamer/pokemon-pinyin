from pkdicts.core import processor
from pkdicts.core.dictionary import ScrapeConfig
from pkdicts.core.parse_page import Selector

page = "特性列表"

selectors = [
    "table.eplist>tbody>tr>td:nth-child(2)>a",  # 中文
    "table.eplist>tbody>tr>td:nth-child(3)>a",  # 日文
    "table.eplist>tbody>tr>td:nth-child(4)>a",  # 英文
]

config = ScrapeConfig(
    name="abilities",
    words=[
        Selector(
            variant="zh-hant",
            page=page,
            element=selectors[0],
            processor=processor.compose(
                processor.NFKC,
                processor.opencc_t2s,
                processor.remove_characters(["・"]),
                processor.remove_repeat,
                processor.remove_token(
                    [
                        "黏著",
                    ],
                ),
            ),
        ),
        Selector(
            variant="zh-hans",
            page=page,
            element=selectors[0],
            processor=processor.compose(
                processor.NFKC,
                processor.remove_repeat,
            ),
        ),
    ],
)
