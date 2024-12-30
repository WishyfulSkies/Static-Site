from textnode import TextNode, TextType
from nodesplitter import split_nodes_delimiter, split_nodes_image, split_nodes_link
import re

def text_to_textnodes(text):
	node = TextNode(text, TextType.TEXT)
	image_nodes = split_nodes_image([node])
	image_link_nodes = split_nodes_link(image_nodes)
	with_bold_nodes = split_nodes_delimiter(image_link_nodes, "**", TextType.BOLD)
	with_italic_nodes = split_nodes_delimiter(with_bold_nodes, "*", TextType.ITALIC)
	total_nodes = split_nodes_delimiter(with_italic_nodes, "`", TextType.CODE)
	return total_nodes

def markdown_to_blocks(markdown):
	blocks = markdown.split("\n\n")
	blocks = list(map(lambda x: x.strip(), blocks))
	nonempty_blocks = []
	for block in blocks:
		if block:
			block_lines = block.split("\n")
			block_lines = list(map(lambda x: x.strip(), block_lines))
			block = "\n".join(block_lines)
			nonempty_blocks.append(block)
	return nonempty_blocks

def block_to_block_type(block):
	if re.match(r"#{1,6}\s.+", block):
		return "heading"
	elif block.startswith("```") and block.endswith("```"):
		return "code"
	lines = block.split("\n")
	count = 0
	for line in lines:
		if line.startswith(">"):
			count += 1
	if count == len(lines) and count != 0:
		return "quote"
	listcount = 0
	for line in lines:
		if line.startswith("* ") or line.startswith("- "):
			listcount += 1
	if listcount == len(lines) and listcount != 0:
		return "unordered_list"
	for i in range(len(lines)):
		if lines[i].startswith(f"{i+1}. "):
			continue
		else:
			return "paragraph"
	return "ordered_list"
		



