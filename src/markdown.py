from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from nodesplitter import split_nodes_delimiter, split_nodes_image, split_nodes_link
import re
import os

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
		
def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	nodes = []
	for block in blocks:
		block_type = block_to_block_type(block)
		textnode_list = text_to_textnodes(block)
		child_nodes = []
		for node in textnode_list:
			if block_type != "heading" and block_type != "quote":
				child_nodes.append(text_node_to_html_node(node))


		if block_type == "paragraph":
			block_node = ParentNode("p", child_nodes)

		elif block_type == "quote":
			clean_text = block[1:].strip()
			cleaned_list = text_to_textnodes(clean_text)
			for node in cleaned_list:
				child_nodes.append(text_node_to_html_node(node))
			block_node = ParentNode("blockquote", child_nodes)

		elif block_type == "code":
			clean_text = block.strip("`")
			code_node = LeafNode("code", clean_text)
			block_node = ParentNode("pre", [code_node])

		elif block_type == "unordered_list":
			list_nodes = []
			items = block.split("\n")
			for item in items:
				item = item[2:].strip()
				text_nodes = text_to_textnodes(item)
				html_nodes = []
				for text_node in text_nodes:
					html_nodes.append(text_node_to_html_node(text_node))
				converted_list_node = ParentNode("li", html_nodes)
				list_nodes.append(converted_list_node)
			block_node = ParentNode("ul", list_nodes)

		elif block_type == "ordered_list":
			list_nodes = []
			items = block.split("\n")
			for item in items:
				dot_position = item.find(". ")
				item = item[dot_position + 2:].strip()
				text_nodes = text_to_textnodes(item)
				html_nodes = []
				for text_node in text_nodes:
					html_nodes.append(text_node_to_html_node(text_node))
				converted_list_node = ParentNode("li", html_nodes)
				list_nodes.append(converted_list_node)
			block_node = ParentNode("ol", list_nodes)

		elif block_type == "heading":
			heading_level = len(block) - len(block.lstrip("#"))
			heading_tag = f"h{heading_level}"
			clean_text = block[heading_level:].strip()
			cleaned_list = text_to_textnodes(clean_text)
			for node in cleaned_list:
				child_nodes.append(text_node_to_html_node(node))
			block_node = ParentNode(heading_tag, child_nodes)

		nodes.append(block_node)
	full_nodes = ParentNode("div", nodes)
	return full_nodes

def extract_title(markdown):
	lines = markdown.split("\n")
	for line in lines:
		stripped_line = line.strip()
		if stripped_line.startswith("# "):
				return stripped_line[2:]
		continue
	raise Exception("No h1 header found")

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	os.makedirs(os.path.dirname(dest_path), exist_ok=True)
	with open(from_path, "r") as file:
		file_contents = file.read()
	with open(template_path, "r") as file:
		template_contents = file.read()

	node = markdown_to_html_node(file_contents)
	node_string = node.to_html()
	title = extract_title(file_contents)
	template_contents = template_contents.replace("{{ Title }}", title)
	template_contents = template_contents.replace("{{ Content }}", node_string)

	with open(dest_path, "w") as output_file:
		output_file.write(template_contents)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	directory_list = os.listdir(dir_path_content)
	for item in directory_list:
		full_path = os.path.join(dir_path_content, item)

		if os.path.isfile(full_path):
			if item.endswith(".md"):
				relative_path = os.path.relpath(full_path, "content")
				html_relative_path = os.path.splitext(relative_path)[0] + ".html"
				html_full_path = os.path.join(dest_dir_path, html_relative_path)
				os.makedirs(os.path.dirname(html_full_path), exist_ok=True)
				generate_page(full_path, template_path, html_full_path)

		if os.path.isdir(full_path):
			generate_pages_recursive(full_path, template_path, dest_dir_path)