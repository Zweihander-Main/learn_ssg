import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter


class TestUtils(unittest.TestCase):
    def test_split_nodes_delim_plain(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], TextNode("This is plain text", TextType.TEXT))

    def test_split_nodes_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            [repr(n) for n in new_nodes],
            [
                "TextNode(This is text with a , TEXT, None)",
                "TextNode(code block, CODE, None)",
                "TextNode( word, TEXT, None)",
            ],
        )
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))
        self.assertEqual(
            [n.text for n in new_nodes],
            ["This is text with a ", "code block", " word"],
        )
        self.assertEqual(
            [n.text_type for n in new_nodes],
            [TextType.TEXT, TextType.CODE, TextType.TEXT],
        )
        self.assertEqual(
            [n.url for n in new_nodes],
            [None, None, None],
        )

    def test_split_nodes_multiple(self):
        node = TextNode("`code1` and `code2`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("code1", TextType.CODE))
        self.assertEqual(new_nodes[1], TextNode(" and ", TextType.TEXT))
        self.assertEqual(new_nodes[2], TextNode("code2", TextType.CODE))

    def test_split_nodes_bold(self):
        node = TextNode("This is *bold* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_split_nodes_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_split_nodes_multiple_mixed(self):
        node = TextNode("This is *bold* and _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter(
            split_nodes_delimiter([node], "*", TextType.BOLD), "_", TextType.ITALIC
        )
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" and ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[4], TextNode(" text", TextType.TEXT))
