import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from nodesplitter import split_nodes_delimiter, split_nodes_image, split_nodes_link


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="p", value="Text thingygubs", props={"href": "https://www.google.com"})
        node2 = HTMLNode(tag="p", value="Text thingygubs", props={"href": "https://www.google.com"})
        self.assertEqual(node, node2)

    def test_neq(self):
        node = HTMLNode("p", "Text thingygubs", {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "Text thingygubs")
        self.assertNotEqual(node, node2)

    def test_novalue(self):
        node = HTMLNode("p", {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "Text thingygubs", {"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)

    def test_tagdif(self):
        node = HTMLNode("div1", "Text thingygubs", {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "Text thingygubs", {"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)

class TestLeafNode(unittest.TestCase):
    def test_basic_paragraph(self):
        node = LeafNode("p", "This is a paragraph.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")

    def test_no_tag(self):
        node = LeafNode(None, "String to display")
        self.assertEqual(node.to_html(), "String to display")

    def test_full_set(self):
        node = LeafNode("a", "Click Here", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click Here</a>')

    def test_value_error(self):
        with self.assertRaises(ValueError):
            node = LeafNode("a", None)
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", None)
            node.to_html()

    def test_output(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_nested_parents(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            )],)
        self.assertEqual(node.to_html(), "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>")

class TestSplitNode(unittest.TestCase):
    def test_nontext(self):
        node = TextNode("**bold**", TextType.BOLD)
        split = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(node.text, split[0].text)

    def test_exception(self):
        with self.assertRaises(Exception):
            node = TextNode("Testing 'code' with 'unclosed code", TextType.TEXT)
            split_node = split_nodes_delimiter([node], "'", TextType.CODE)

    def test_multiple_delimiters(self):
        node = TextNode("'Code' and more 'code'", TextType.TEXT)
        split_node = split_nodes_delimiter([node], "'", TextType.CODE)
        self.assertEqual(len(split_node), 3)
        self.assertEqual(split_node[0].text, "Code")
        self.assertEqual(split_node[0].text_type, TextType.CODE)
        self.assertEqual(split_node[1].text, " and more ")
        self.assertEqual(split_node[1].text_type, TextType.TEXT)
        self.assertEqual(split_node[2].text, "code")
        self.assertEqual(split_node[2].text_type, TextType.CODE)

class TestSplitImages(unittest.TestCase):
    def test_emptynodes(self):
        node = TextNode("", TextType.TEXT)
        split = split_nodes_image([node])
        self.assertEqual(len(split), 0)

    def test_oneimage(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        split = split_nodes_image([node])
        self.assertEqual(split,
                         [TextNode("This is text with a ", TextType.TEXT),
                          TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                          ])

    def test_twoimages(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        split = split_nodes_image([node])
        self.assertEqual(split,
                         [TextNode("This is text with a ", TextType.TEXT),
                          TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                          TextNode(" and ", TextType.TEXT),
                          TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
                          ])


class TestSplitLinks(unittest.TestCase):
    def test_emptynodes(self):
        node = TextNode("", TextType.TEXT)
        split = split_nodes_link([node])
        self.assertEqual(len(split), 0)

    def test_onelink(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        split = split_nodes_link([node])
        self.assertEqual(split,
                         [TextNode("This is text with a link ", TextType.TEXT),
                          TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")]
                         )

    def test_twolinks(self):
        node = TextNode(
                        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                        TextType.TEXT,
                        )
        split = split_nodes_link([node])
        self.assertEqual(split,
                        [TextNode("This is text with a link ", TextType.TEXT),
                        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),     
                        TextNode(" and ", TextType.TEXT),
                        TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
                        ])

if __name__ == "__main__":
    unittest.main()
