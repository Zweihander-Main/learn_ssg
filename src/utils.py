import re

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
