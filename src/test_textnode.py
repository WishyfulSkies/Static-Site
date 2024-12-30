import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is node 1", TextType.BOLD)
        node2 = TextNode("This is node 2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_urlblank(self):
        node = TextNode("This is a node", TextType.CODE, None)
        node2 = TextNode("This is a node", TextType.CODE)
        self.assertEqual(node, node2)

    def test_urldif(self):
        node = TextNode("This is a node", TextType.IMAGE, "website.link.net")
        node2 =  TextNode("This is a node", TextType.IMAGE, "website.wrong.net")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a normal node", TextType.TEXT)
        changed_node = text_node_to_html_node(node)
        self.assertEqual(changed_node.to_html(), "This is a normal node")

    def test_image(self):
        node = TextNode("Pretty cat photo", TextType.IMAGE, "google.com/cutecatto")
        changed_node = text_node_to_html_node(node)
        self.assertEqual(changed_node.to_html(), '<img src="google.com/cutecatto" alt="Pretty cat photo"></img>')

    def test_typeerror(self):
        with self.assertRaises(Exception):
            node = TextNode("This is a faulty node", "FAKE_TYPE")
            changed_node = text_node_to_html_node(node)
            changed_node.to_html()


if __name__ == "__main__":
    unittest.main()
