import unittest

from extraction import extract_markdown_images, extract_markdown_links


class TestMarkdownLinks(unittest.TestCase):
    def test_falseinput(self):
        self.assertEqual(extract_markdown_links(""),[])

    def test_multipleimages(self):
        link_tuples = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(link_tuples,
                         [("to boot dev", "https://www.boot.dev"),
                          ("to youtube", "https://www.youtube.com/@bootdotdev")
                          ])
        
    def test_noimages(self):
        self.assertEqual([],extract_markdown_links("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"))

class TestMarkdownImages(unittest.TestCase):
    def test_falseinput(self):
        self.assertEqual(extract_markdown_images(""),[])

    def test_multipleimages(self):
        link_tuples = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(link_tuples,
                         [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                          ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
                          ])

    def test_nolinks(self):
        self.assertEqual([],extract_markdown_images("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"))