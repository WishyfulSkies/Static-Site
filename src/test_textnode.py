import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
