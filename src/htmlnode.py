from __future__ import annotations

from collections.abc import Sequence
from typing import cast, override


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: Sequence[object] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag: str | None = tag
        self.value: str | None = value
        if children is not None:
            if not all(isinstance(c, HTMLNode) for c in children):
                raise ValueError("children must be a list of HTMLNode or None")
            childrenCast: Sequence[HTMLNode] = cast(Sequence[HTMLNode], children)
            self.children: Sequence[HTMLNode] | None = childrenCast
        else:
            self.children = None
        self.props: dict[str, str] | None = props

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented yet")

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())

    @override
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        value: str,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag=tag, value=value, children=None, props=props)

    @override
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        props_str = self.props_to_html()
        if props_str:
            return f"<{self.tag} {props_str}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"

    @override
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: Sequence[HTMLNode | LeafNode],
        props: dict[str, str] | None = None,
    ) -> None:
        childrenCast: list[object] = cast(list[object], children)
        super().__init__(tag=tag, value=None, children=childrenCast, props=props)

    @override
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        props_str = self.props_to_html()
        children_html = "".join(child.to_html() for child in self.children or [])
        if props_str:
            return f"<{self.tag} {props_str}>{children_html}</{self.tag}>"
        return f"<{self.tag}>{children_html}</{self.tag}>"

    @override
    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
