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
            print(len(parts), start, alt_text, url, last_end)
            if start > last_end:
                new_nodes.append(TextNode(node.text[last_end:start], TextType.TEXT))
            new_nodes.append(TextNode(text=alt_text, text_type=TextType.IMAGE, url=url))
            last_end = start + len(search_string)
            print(new_nodes)
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
