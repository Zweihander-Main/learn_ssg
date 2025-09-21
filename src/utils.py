import re
from enum import Enum

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
