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

        node_no_url = TextNode("No link", TextType.TEXT)
        self.assertIsNone(node_no_url.url)

    def test_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_to_html_node_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(
            html_node.to_html(),
            "<b>This is bold text</b>",
        )

    def test_to_html_node_link(self):
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://example.com">Click here</a>',
        )

    def test_to_html_node_link_no_url(self):
        node = TextNode("Broken link", TextType.LINK)
        with self.assertRaises(ValueError):
            _ = node.to_html_node()

    def test_to_html_node_image(self):
        node = TextNode("", TextType.IMAGE, url="https://example.com/image.png")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://example.com/image.png", "alt": ""}
        )
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://example.com/image.png" alt=""/>',
        )

    def test_to_html_node_image_no_url(self):
        node = TextNode("Broken image", TextType.IMAGE)
        with self.assertRaises(ValueError):
            _ = node.to_html_node()


if __name__ == "__main__":
    _ = unittest.main()
