from pkdicts.core import processor
from pkdicts.core.dictionary import ScrapeConfig
from pkdicts.core.parse_page import Selector

page = "宝可梦列表（按全国图鉴编号）/简单版"  # noqa: RUF001

selectors = [
    "table.eplist>tbody>tr>td:nth-child(2)>a",  # 中文
    "table.eplist>tbody>tr>td:nth-child(3)>a",  # 日文
    "table.eplist>tbody>tr>td:nth-child(4)>a",  # 英文
]

config = ScrapeConfig(
    name="pokemon",
    words=[
        Selector(
            variant="zh-hans",
            page=page,
            element=selectors[0],
            processor=processor.compose(
                processor.NFKC,
                processor.remove_characters(["・", ":"]),
            ),
        ),
        Selector(
            variant="zh-hant",
            page=page,
            element=selectors[0],
            processor=processor.compose(
                processor.fork(
                    processor.replace_characters(
                        {
                            "Ⅱ": "2",
                        },
                    ),
                    processor.noop,
                ),
                processor.fw_latin_to_hw,
                processor.opencc_t2s,
                processor.replace_characters(
                    {
                        ":": "：",  # noqa: RUF001
                    },
                ),
                processor.remove_token(
                    ["火爆兽", "萤光鱼", "保母虫", "车轮毬", "保母曼波", "穿著熊"],
                ),
            ),
        ),
    ],
    translates=[
        Selector(
            variant="zh-hans",
            page=page,
            element=selectors[1],
        ),
        Selector(
            variant="zh-hans",
            page=page,
            element=selectors[2],
            processor=processor.replace_characters(
                {
                    " ": "\N{NO-BREAK SPACE}",
                },
            ),
        ),
    ],
)
