import unittest

from markdown import text_to_textnodes, markdown_to_blocks, block_to_block_type
from textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_empty(self):
        text = ""
        converted = text_to_textnodes(text)
        self.assertEqual([], converted)

    def test_longlist(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        converted = text_to_textnodes(text)
        self.assertEqual(converted,
                         [
                        TextNode("This is ", TextType.TEXT),
                        TextNode("text", TextType.BOLD),
                        TextNode(" with an ", TextType.TEXT),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word and a ", TextType.TEXT),
                        TextNode("code block", TextType.CODE),
                        TextNode(" and an ", TextType.TEXT),
                        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ", TextType.TEXT),
                        TextNode("link", TextType.LINK, "https://boot.dev"),
                        ]
                        )
        
class TestMarkdownToBlocks(unittest.TestCase):
    def test_empty(self):
        text = ""
        converted = markdown_to_blocks(text)
        self.assertEqual([],converted)

    def test_text(self):
        text = """# This is a heading

                  
                   This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                    * This is the first list item in a list block
                * This is a list item
                * This is another list item"""
        converted = markdown_to_blocks(text)
        self.assertEqual(converted,["# This is a heading",
                                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                                    "* This is the first list item in a list block\n* This is a list item\n* This is another list item"]
                                    )
        
    def test_headertext(self):
        text = """# Header

        Para 1

        * List 1
            * List 2
                * List 3"""
        converted = markdown_to_blocks(text)
        self.assertEqual(converted, ["# Header",
                                     "Para 1",
                                     "* List 1\n* List 2\n* List 3"]
                                     )

class TestBlockToBlockType(unittest.TestCase):
    def test_emptystring(self):
        block = ""
        result = block_to_block_type(block)
        self.assertEqual("paragraph", result)

    def test_orderedlist(self):
        block = "1. First\n2. Second\n3. Third"
        result = block_to_block_type(block)
        self.assertEqual("ordered_list", result)

    def test_heading(self):
        block = "#### Heading Test"
        result = block_to_block_type(block)
        self.assertEqual("heading", result)

    def test_unorderedlist(self):
        block = "* List item\n- Another item\n* Last item"
        result = block_to_block_type(block)
        self.assertEqual("unordered_list", result)

    def test_code(self):
        block = "``` Code stuffs   ```"
        result = block_to_block_type(block)
        result = self.assertEqual("code", result)

if __name__ == "__main__":
    unittest.main()