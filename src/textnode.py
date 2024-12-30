from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
	TEXT = "normal"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

class TextNode():
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(Node1, Node2):
		if Node1.text == Node2.text:
			if Node1.text_type == Node2.text_type:
				if Node1.url == Node2.url:
					return True
		return False

	def __repr__(node):
		return f"TextNode({node.text}, {node.text_type.value}, {node.url})"

def text_node_to_html_node(text_node):
	if text_node.text_type == TextType.TEXT:
		new_node = LeafNode(None, text_node.text)
	elif text_node.text_type == TextType.BOLD:
		new_node = LeafNode("b", text_node.text)
	elif text_node.text_type == TextType.ITALIC:
		new_node = LeafNode("i", text_node.text)
	elif text_node.text_type == TextType.CODE:
		new_node = LeafNode("code", text_node.text)
	elif text_node.text_type == TextType.LINK:
		new_node = LeafNode("a", text_node.text, {"href": text_node.url})
	elif text_node.text_type == TextType.IMAGE:
		new_node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
	else:
		raise Exception("Invalid TextType supplied to text node to HTMLNode conversion")
	return new_node
