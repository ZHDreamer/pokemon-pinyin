from pkdicts.core import processor
from pkdicts.core.dictionary import ScrapeConfig
from pkdicts.core.parse_page import Selector

page = "地点列表"

selectors = [
    "table.eplist>tbody>tr>td:nth-child(1)>a",  # 中文
    "table.eplist>tbody>tr>td:nth-child(2)>a",  # 日文
    "table.eplist>tbody>tr>td:nth-child(3)>a",  # 英文
]

config = ScrapeConfig(
    name="locations",
    words=[
        Selector(
            variant="zh-hans",
            page=page,
            element=selectors[0],
            extractor=lambda el: list(el.stripped_strings),
            processor=processor.compose(
                processor.remove_prefix_by_keywords(["异次元密阿雷："]),  # noqa: RUF001
                processor.remove_suffix_by_keywords(["（黑／白）", "（黑２／白２）"]),  # noqa: RUF001
                processor.NFKC,
                processor.remove_repeat,
            ),
        ),
    ],
)
