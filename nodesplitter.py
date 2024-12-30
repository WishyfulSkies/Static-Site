from textnode import TextNode, TextType
from htmlnode import HTMLNode
from extraction import extract_markdown_images, extract_markdown_links
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_node = node.text.split(delimiter)
            if len(split_node) % 2 == 0:
                raise Exception("Invalid markdown: unclosed delimiter")
            for i in range(0,len(split_node)):
                if split_node[i] != "":
                    if i % 2 != 0:
                        new_nodes.append(TextNode(split_node[i], text_type))
                    else:
                        new_nodes.append(TextNode(split_node[i], TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        image_matches = extract_markdown_images(node.text) 
        for alt_text, image_url in image_matches:
            sections = node.text.split(f"![{alt_text}]({image_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
            node.text = sections[1]
        if node.text != "":
            new_nodes.append(TextNode(node.text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        link_matches = extract_markdown_links(node.text)
        for anchor_text, image_url in link_matches:
            sections = node.text.split(f"[{anchor_text}]({image_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, image_url))
            node.text = sections[1]
        if node.text != "":
            new_nodes.append(TextNode(node.text, TextType.TEXT))
    return new_nodes