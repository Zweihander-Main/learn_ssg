import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("Node 1", TextType.BOLD)
        node2 = TextNode("Node 2", TextType.BOLD)
        self.assertNotEqual(node, node2)

        node3 = TextNode("Node 1", TextType.ITALIC)
        self.assertNotEqual(node, node3)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, BOLD, None)")

    def test_url(self):
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        self.assertEqual(node.url, "https://example.com")

        node_no_url = TextNode("No link", TextType.PLAIN)
        self.assertIsNone(node_no_url.url)


if __name__ == "__main__":
    _ = unittest.main()
