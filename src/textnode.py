from enum import Enum

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
