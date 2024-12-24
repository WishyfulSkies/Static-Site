import unittest

from htmlnode import HTMLNode, LeafNode


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

if __name__ == "__main__":
    unittest.main()
