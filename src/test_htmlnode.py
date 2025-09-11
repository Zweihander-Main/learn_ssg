import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("div", "Content", None, {"class": "my-class"})

        with self.assertRaises(NotImplementedError):
            _ = node.to_html()

    def test_props_to_html(self):
        node = HTMLNode("div", "Content", None, {"class": "my-class", "id": "my-id"})
        self.assertEqual(node.props_to_html(), 'class="my-class" id="my-id"')

        node_no_props = HTMLNode("div", "Content")
        self.assertEqual(node_no_props.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("div", "Content", None, {"class": "my-class"})
        self.assertEqual(
            repr(node), "HTMLNode(div, Content, None, {'class': 'my-class'})"
        )

    def test_no_tag(self):
        node = HTMLNode(value="Just text")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Just text")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        self.assertEqual(repr(node), "HTMLNode(None, Just text, None, None)")
        self.assertEqual(node.props_to_html(), "")

    def test_no_value(self):
        node = HTMLNode(tag="span", children=[], props={"style": "color:red;"})
        self.assertEqual(node.tag, "span")
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"style": "color:red;"})
        self.assertEqual(
            repr(node), "HTMLNode(span, None, [], {'style': 'color:red;'})"
        )
        self.assertEqual(node.props_to_html(), 'style="color:red;"')

    def test_no_children(self):
        node = HTMLNode(tag="p", value="Paragraph", props={"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Paragraph")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"class": "text"})

    def test_no_props(self):
        node = HTMLNode(tag="a", value="Link", children=[])
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Link")
        self.assertEqual(node.children, [])
        self.assertIsNone(node.props)
        self.assertEqual(repr(node), "HTMLNode(a, Link, [], None)")
        self.assertEqual(node.props_to_html(), "")
