from enum import Enum
from typing import override

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = 1
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

    def to_html_node(self) -> LeafNode:
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(tag=None, value=self.text)
            case TextType.BOLD:
                return LeafNode(tag="strong", value=self.text)
            case TextType.ITALIC:
                return LeafNode(tag="em", value=self.text)
            case TextType.UNDERLINE:
                return LeafNode(tag="u", value=self.text)
            case TextType.STRIKETHROUGH:
                return LeafNode(tag="s", value=self.text)
            case TextType.LINK:
                if self.url is None:
                    raise ValueError("Link text node must have a URL")
                return LeafNode(tag="a", value=self.text, props={"href": self.url})
            case TextType.CODE:
                return LeafNode(tag="code", value=self.text)
            case TextType.CODE_BLOCK:
                return LeafNode(tag="pre", value=self.text)
            case TextType.QUOTE:
                return LeafNode(tag="blockquote", value=self.text)
            case TextType.HIGHLIGHT:
                return LeafNode(tag="mark", value=self.text)
            case TextType.IMAGE:
                if self.url is None:
                    raise ValueError("Image text node must have a URL")
                return LeafNode(
                    tag="img", value="", props={"src": self.url, "alt": self.text}
                )
            case TextType.LIST_ITEM:
                return LeafNode(tag="li", value=self.text)
            case TextType.HEADING1:
                return LeafNode(tag="h1", value=self.text)
            case TextType.HEADING2:
                return LeafNode(tag="h2", value=self.text)
            case TextType.HEADING3:
                return LeafNode(tag="h3", value=self.text)
            case TextType.HEADING4:
                return LeafNode(tag="h4", value=self.text)
            case TextType.HEADING5:
                return LeafNode(tag="h5", value=self.text)
            case TextType.HEADING6:
                return LeafNode(tag="h6", value=self.text)
            case _:  # pyright: ignore[reportUnnecessaryComparison]
                raise ValueError(f"Unsupported text type: {self.text_type}")  # pyright: ignore[reportUnreachable]

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
