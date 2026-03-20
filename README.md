# pkdicts

pkdicts 是一个宝可梦 rime 词库，数据来源[神奇宝贝百科 52 Poke](https://wiki.52poke.com/wiki/主页)

## 词库

| 文件名        | 来源                                                                           | 说明                         |
| :------------ | :----------------------------------------------------------------------------- | :--------------------------- |
| pk_abilities  | [特性列表](https://wiki.52poke.com/wiki/特性列表)                              |                              |
| pk_characters | [游戏人物列表](https://wiki.52poke.com/wiki/游戏人物列表)                      |                              |
| pk_items      | [道具列表](https://wiki.52poke.com/wiki/道具列表)                              |                              |
| pk_locations  | [地点列表](https://wiki.52poke.com/wiki/地点列表)                              |                              |
| pk_moves      | [招式列表](https://wiki.52poke.com/wiki/招式列表)                              |                              |
| pk_pokemon    | [宝可梦列表](https://wiki.52poke.com/wiki/宝可梦列表（按全国图鉴编号）/简单版) | [宝可梦名称](doc/Pokemon.md) |

## OpenCC

Pokemon 列表附加了日语和英语名称，可用于查找外文攻略等。

因为 opencc 本身的限制，利用空格作为分隔符，英文中的空格被替换为不间断空格（`U+00A0`）。一般情况下用于搜索不会有问题，但是如果用于写作，请注意这一点。

如添加 opencc，请在 `emoji.json` 字段中添加以下内容：

```json
{
    …
    "conversion_chain": [
        {
            "dict": {
                "type": "group",
                "dicts": [
                    {
                        "type": "text",
                        "file": "pokemon.txt"
                    },
                    …
                ]
            }
        }
    ]
}
```

## 安装

TODO

## 开发

安装依赖

```bash
uv sync
```

生成词库

```bash
uv run pkdicts --all
```

## 许可

本项目代码采用 [GPL-3.0](LICENSE) 许可。

词库文件采用 [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/deed.zh-hans) 许可，
数据来源于[神奇宝贝百科 52 Poke](https://wiki.52poke.com/wiki/主页)，
该网站内容采用 [CC BY-NC-SA 3.0](https://wiki.52poke.com/wiki/神奇宝贝百科:版权声明) 许可。
