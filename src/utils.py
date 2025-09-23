import re
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """
    Splits text nodes in old_nodes by the given delimiter and assigns the specified text_type
    to the parts between the delimiters.

    Args:
        old_nodes (list[TextNode]): List of TextNode objects to be processed.
        delimiter (str): The delimiter string to split the text.
        text_type (TextType): The TextType to assign to the parts between delimiters.

    Returns:
        list[TextNode]: A new list of TextNode objects with the text split and types
                        assigned accordingly.
    """
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if part:
                if i % 2 == 0:  # avoid including delimiter
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """
    Extracts markdown image links from the given text.

    Args:
        text (str): The input text containing markdown image links.

    Returns:
        list[tuple[str, str]]: A list of tuples where each tuple contains the alt text and URL of an image.
    """
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """
    Extracts markdown links from the given text.

    Args:
        text (str): The input text containing markdown links.

    Returns:
        list[tuple[str, str]]: A list of tuples where each tuple contains the link text and URL.
    """
    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits text nodes in old_nodes by markdown image links and assigns the IMAGE text_type
    to the image parts.

    Args:
        old_nodes (list[TextNode]): List of TextNode objects to be processed.

    Returns:
        list[TextNode]: A new list of TextNode objects with the text split and types
                        assigned accordingly.
    """
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = extract_markdown_images(node.text)
        if not parts:
            new_nodes.append(node)
            continue
        last_end = 0
        for alt_text, url in parts:
            search_string = f"![{alt_text}]({url})"
            start = node.text.find(search_string, last_end)
            if start > last_end:
                new_nodes.append(TextNode(node.text[last_end:start], TextType.TEXT))
            new_nodes.append(TextNode(text=alt_text, text_type=TextType.IMAGE, url=url))
            last_end = start + len(search_string)
        if last_end < len(node.text):
            new_nodes.append(TextNode(node.text[last_end:], TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits text nodes in old_nodes by markdown links and assigns the LINK text_type
    to the link parts.

    Args:
        old_nodes (list[TextNode]): List of TextNode objects to be processed.

    Returns:
        list[TextNode]: A new list of TextNode objects with the text split and types
                        assigned accordingly.
    """
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = extract_markdown_links(node.text)
        if not parts:
            new_nodes.append(node)
            continue
        last_end = 0
        for link_text, url in parts:
            search_string = f"[{link_text}]({url})"
            start = node.text.find(search_string, last_end)
            if start > last_end:
                new_nodes.append(TextNode(node.text[last_end:start], TextType.TEXT))
            new_nodes.append(TextNode(text=link_text, text_type=TextType.LINK, url=url))
            last_end = start + len(search_string)
        if last_end < len(node.text):
            new_nodes.append(TextNode(node.text[last_end:], TextType.TEXT))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    """
    Converts a plain text string into a list of TextNode objects split using markdown syntax.

    Args:
        text (str): The input plain text string.

    Returns:
        list[TextNode]: A list of TextNode objects representing the parsed text.
    """
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "__", TextType.UNDERLINE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "~~", TextType.STRIKETHROUGH)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Converts a markdown string into a list of text blocks split by double newlines.

    Args:
        markdown (str): The input markdown string.

    Returns:
        list[str]: A list of text blocks.
    """
    blocks = [block.strip() for block in markdown.split("\n\n") if block.strip()]
    return blocks


BlockType = Enum(
    "BlockType",
    ["paragraph", "heading", "code", "quote", "unordered_list", "ordered_list"],
)


def block_to_block_type(block: str) -> BlockType:
    """
    Determines the type of a markdown block.

    Args:
        block (str): The input markdown block.

    Returns:
        BlockType: The type of the block.
    """
    if re.match(r"^#{1,6} ", block):
        return BlockType.heading
    elif re.match(r"^```", block):
        return BlockType.code
    elif re.match(r"^> ", block):
        return BlockType.quote
    elif re.match(r"^(\*|\-|\+) ", block):
        return BlockType.unordered_list
    elif re.match(r"^\d+\. ", block):
        return BlockType.ordered_list
    else:
        return BlockType.paragraph


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    """
    Converts a TextNode into an HTMLNode.

    Args:
        text_node (TextNode): The input TextNode object.

    Returns:
        HTMLNode: The corresponding HTMLNode object.
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.UNDERLINE:
            return LeafNode(tag="u", value=text_node.text)
        case TextType.STRIKETHROUGH:
            return LeafNode(tag="s", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a",
                props={"href": text_node.url if text_node.url else "#"},
                value=text_node.text,
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                props={
                    "src": text_node.url if text_node.url else "",
                    "alt": text_node.text,
                },
                value="",
            )
        case _:
            return LeafNode(tag=None, value=text_node.text)


def text_to_children(text: str) -> list[HTMLNode]:
    """
    Converts a plain text string into a list of HTMLNode children.

    Args:
        text (str): The input plain text string.

    Returns:
        list[HTMLNode]: A list of HTMLNode objects representing the parsed text.
    """
    text_nodes = text_to_textnodes(text)
    children: list[HTMLNode] = []
    for tn in text_nodes:
        children.append(text_node_to_html_node(tn))
    return children


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    Converts a markdown string into an HTMLNode tree.

    Args:
        markdown (str): The input markdown string.

    Returns:
        HTMLNode: The root HTMLNode representing the parsed markdown.
    """
    blocks = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.heading:
                heading_match = re.match(r"^(#{1,6}) (.*)", block)
                level = 1  # Default to level 1
                heading_text = ""
                if heading_match:
                    level = len(heading_match.group(1))
                    heading_text = heading_match.group(2).strip().replace("\n", " ")
                node = ParentNode(
                    tag=f"h{level}",
                    children=text_to_children(heading_text),
                )
                children.append(node)

            case BlockType.paragraph:
                node = ParentNode(
                    tag="p",
                    children=text_to_children(block.strip().replace("\n", " ")),
                )
                children.append(node)

            case BlockType.unordered_list:
                items_ul: list[tuple[str, str]] = re.findall(
                    r"^(\*|\-|\+) (.+)$", block, re.MULTILINE
                )
                li_children: list[ParentNode] = []
                for _, item in items_ul:
                    li_node = ParentNode(
                        tag="li",
                        children=text_to_children(item.strip().replace("\n", " ")),
                    )
                    li_children.append(li_node)
                ul_node = ParentNode(tag="ul", children=li_children)
                children.append(ul_node)

            case BlockType.ordered_list:
                items_ol: list[str] = re.findall(r"^\d+\. (.+)$", block, re.MULTILINE)
                li_children = []
                for item in items_ol:
                    li_node = ParentNode(
                        tag="li",
                        children=text_to_children(item.strip().replace("\n", " ")),
                    )
                    li_children.append(li_node)
                ol_node = ParentNode(tag="ol", children=li_children)
                children.append(ol_node)

            case BlockType.quote:
                quote_match = re.match(r"^> (.+)$", block, re.MULTILINE)
                content = quote_match.group(1).strip() if quote_match else block.strip()
                node = ParentNode(
                    tag="blockquote",
                    children=text_to_children(content.replace("\n> ", " ")),
                )
                children.append(node)

            case BlockType.code:
                code_match = re.match(r"^```(\w+)?\n([\s\S]+?\n)```$", block)
                if code_match:
                    language = code_match.group(1) if code_match.group(1) else ""
                    code_content = code_match.group(2)
                else:
                    language = ""
                    code_content = block
                code_node = ParentNode(
                    tag="code",
                    props={"class": f"language-{language}"} if language else {},
                    children=[LeafNode(tag=None, value=code_content)],
                )
                pre_node = ParentNode(tag="pre", children=[code_node])
                children.append(pre_node)

    return ParentNode(tag="div", children=children)
