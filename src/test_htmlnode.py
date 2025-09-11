import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html(self):
        node = LeafNode("b", "Bold Text", {"class": "bold"})
        self.assertEqual(node.to_html(), '<b class="bold">Bold Text</b>')

        node_no_props = LeafNode("i", "Italic Text")
        self.assertEqual(node_no_props.to_html(), "<i>Italic Text</i>")

    def test_to_html_no_value(self):
        node = LeafNode("span", None)  # pyright: ignore[reportArgumentType]
        with self.assertRaises(ValueError):
            _ = node.to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, "No Tag")  # pyright: ignore[reportArgumentType]
        self.assertEqual(node.to_html(), "No Tag")

    def test_repr(self):
        node = LeafNode("b", "Bold Text", {"class": "bold"})
        self.assertEqual(repr(node), "LeafNode(b, Bold Text, {'class': 'bold'})")


class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        child1 = LeafNode("li", "Item 1")
        child2 = LeafNode("li", "Item 2")
        parent = ParentNode("ul", [child1, child2], {"class": "list"})

        self.assertEqual(
            parent.to_html(), '<ul class="list"><li>Item 1</li><li>Item 2</li></ul>'
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])  # pyright: ignore[reportArgumentType]
        with self.assertRaises(ValueError):
            _ = parent_node.to_html()

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)  # pyright: ignore[reportArgumentType]
        with self.assertRaises(ValueError):
            _ = parent_node.to_html()

    def test_repr(self):
        child1 = LeafNode("li", "Item 1")
        child2 = LeafNode("li", "Item 2")
        parent = ParentNode("ul", [child1, child2], {"class": "list"})
        self.assertEqual(
            repr(parent),
            "ParentNode(ul, [LeafNode(li, Item 1, None), LeafNode(li, Item 2, None)], {'class': 'list'})",
        )

    def test_empty_children(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")
        self.assertEqual(repr(parent), "ParentNode(div, [], None)")

    def test_lots_of_children(self):
        children = [LeafNode("p", f"Paragraph {i}") for i in range(100)]
        parent = ParentNode("div", children)
        expected_html = (
            "<div>" + "".join(f"<p>Paragraph {i}</p>" for i in range(100)) + "</div>"
        )
        self.assertEqual(parent.to_html(), expected_html)
        self.assertEqual(
            repr(parent),
            f"ParentNode(div, [{', '.join(repr(child) for child in children)}], None)",
        )
