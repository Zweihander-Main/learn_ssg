import unittest

from textnode import TextNode, TextType
from utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "Images: ![img1](http://example.com/1.png) and ![img2](http://example.com/2.jpg)"
        )
        self.assertListEqual(
            [
                ("img1", "http://example.com/1.png"),
                ("img2", "http://example.com/2.jpg"),
            ],
            matches,
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This text has no images.")
        self.assertListEqual([], matches)

    def text_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a [link](https://example.com) in text."
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "Links: [Google](https://google.com) and [OpenAI](https://openai.com)"
        )
        self.assertListEqual(
            [("Google", "https://google.com"), ("OpenAI", "https://openai.com")],
            matches,
        )

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This text has no links.")
        self.assertListEqual([], matches)

    def test_split_images_basic(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) to test",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" to test", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_none(self):
        node = TextNode("This text has no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("Image1: ![img1](http://example.com/1.png)", TextType.TEXT),
            TextNode(" and some text ", TextType.TEXT),
            TextNode("Image2: ![img2](http://example.com/2.jpg)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Image1: ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "http://example.com/1.png"),
                TextNode(" and some text ", TextType.TEXT),
                TextNode("Image2: ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "http://example.com/2.jpg"),
            ],
            new_nodes,
        )

    def test_split_images_adjacent(self):
        node = TextNode(
            "Adjacent images: ![img1](http://example.com/1.png)![img2](http://example.com/2.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Adjacent images: ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "http://example.com/1.png"),
                TextNode("img2", TextType.IMAGE, "http://example.com/2.jpg"),
            ],
            new_nodes,
        )

    def test_split_images_at_ends(self):
        node = TextNode(
            "![start](http://example.com/start.png) Middle text ![end](http://example.com/end.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "http://example.com/start.png"),
                TextNode(" Middle text ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "http://example.com/end.png"),
            ],
            new_nodes,
        )

    def test_split_images_only_image(self):
        node = TextNode(
            "![only](http://example.com/only.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("only", TextType.IMAGE, "http://example.com/only.png"),
            ],
            new_nodes,
        )

    def test_split_images_empty_text(self):
        node = TextNode(
            "",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_no_alt_text(self):
        node = TextNode(
            "This is an image with no alt text ![](http://example.com/noalt.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is an image with no alt text ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "http://example.com/noalt.png"),
            ],
            new_nodes,
        )

    def test_split_images_complex(self):
        node = TextNode(
            "Start ![img1](http://example.com/1.png) middle ![img2](http://example.com/2.jpg) end ![img3](http://example.com/3.gif)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "http://example.com/1.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "http://example.com/2.jpg"),
                TextNode(" end ", TextType.TEXT),
                TextNode("img3", TextType.IMAGE, "http://example.com/3.gif"),
            ],
            new_nodes,
        )

    def test_split_images_special_characters(self):
        node = TextNode(
            "Special chars ![img!@#](http://example.com/!@#.png) in alt text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Special chars ", TextType.TEXT),
                TextNode("img!@#", TextType.IMAGE, "http://example.com/!@#.png"),
                TextNode(" in alt text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_multiline(self):
        node = TextNode(
            "Image on new line:\n![img](http://example.com/img.png)\nEnd of text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image on new line:\n", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "http://example.com/img.png"),
                TextNode("\nEnd of text.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_no_spaces(self):
        node = TextNode(
            "No spaces![img1](http://example.com/1.png)![img2](http://example.com/2.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("No spaces", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "http://example.com/1.png"),
                TextNode("img2", TextType.IMAGE, "http://example.com/2.jpg"),
            ],
            new_nodes,
        )

    def test_split_links_basic(self):
        node = TextNode(
            "This is a [link](https://example.com) in text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" in text.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        node = TextNode("This text has no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("Link1: [Google](https://google.com)", TextType.TEXT),
            TextNode(" and some text ", TextType.TEXT),
            TextNode("Link2: [OpenAI](https://openai.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Link1: ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" and some text ", TextType.TEXT),
                TextNode("Link2: ", TextType.TEXT),
                TextNode("OpenAI", TextType.LINK, "https://openai.com"),
            ],
            new_nodes,
        )

    def test_split_links_adjacent(self):
        node = TextNode(
            "Adjacent links: [Google](https://google.com)[OpenAI](https://openai.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Adjacent links: ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode("OpenAI", TextType.LINK, "https://openai.com"),
            ],
            new_nodes,
        )

    def test_split_links_at_ends(self):
        node = TextNode(
            "[Start](https://start.com) Middle text [End](https://end.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start", TextType.LINK, "https://start.com"),
                TextNode(" Middle text ", TextType.TEXT),
                TextNode("End", TextType.LINK, "https://end.com"),
            ],
            new_nodes,
        )

    def test_split_links_only_link(self):
        node = TextNode(
            "[Only](https://only.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Only", TextType.LINK, "https://only.com"),
            ],
            new_nodes,
        )

    def test_split_links_empty_text(self):
        node = TextNode(
            "",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_complex(self):
        node = TextNode(
            "Start [Google](https://google.com) middle [OpenAI](https://openai.com) end [GitHub](https://github.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("OpenAI", TextType.LINK, "https://openai.com"),
                TextNode(" end ", TextType.TEXT),
                TextNode("GitHub", TextType.LINK, "https://github.com"),
            ],
            new_nodes,
        )

    def test_split_links_special_characters(self):
        node = TextNode(
            "Special chars [link!@#](https://example.com/!@#) in link text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Special chars ", TextType.TEXT),
                TextNode("link!@#", TextType.LINK, "https://example.com/!@#"),
                TextNode(" in link text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_multiline(self):
        node = TextNode(
            "Link on new line:\n[Example](https://example.com)\nEnd of text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link on new line:\n", TextType.TEXT),
                TextNode("Example", TextType.LINK, "https://example.com"),
                TextNode("\nEnd of text.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_no_spaces(self):
        node = TextNode(
            "No spaces![Google](https://google.com)[OpenAI](https://openai.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("No spaces!", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode("OpenAI", TextType.LINK, "https://openai.com"),
            ],
            new_nodes,
        )

    def test_split_links_image(self):
        node = TextNode(
            "This is a [link](https://example.com) in text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" in text.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_plain(self):
        text = "This is plain text."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], TextNode(text, TextType.TEXT))

    def test_text_to_textnodes_complex(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )
