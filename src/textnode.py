from enum import Enum
from typing import override


class TextType(Enum):
    PLAIN = 1
    BOLD = 2
    ITALIC = 3
    UNDERLINE = 4
    STRIKETHROUGH = 5
    LINK = 6
    CODE = 7
    CODE_BLOCK = 8
    QUOTE = 9
    HIGHLIGHT = 10
    IMAGE = 11
    LIST_ITEM = 12
    HEADING1 = 13
    HEADING2 = 14
    HEADING3 = 15
    HEADING4 = 16
    HEADING5 = 17
    HEADING6 = 18


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    @override
    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, TextNode)
            and self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    @override
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.name}, {self.url})"
