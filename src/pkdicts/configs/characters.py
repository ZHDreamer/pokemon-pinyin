from pkdicts.core import processor
from pkdicts.core.dictionary import ScrapeConfig
from pkdicts.core.parse_page import Selector

page = "游戏人物列表"

selectors = [
    "table.eplist>tbody>tr>td:nth-child(1)>a",  # 中文
    "table.eplist>tbody>tr>td:nth-child(2)>a",  # 日文
    "table.eplist>tbody>tr>td:nth-child(3)>a",  # 英文
]

config = ScrapeConfig(
    name="characters",
    words=[
        Selector(
            variant="zh-hans",
            page=page,
            element=selectors[0],
            processor=processor.compose(
                processor.NFKC,
                processor.remove_single_char,
                processor.remove_repeat,
            ),
        ),
    ],
)
