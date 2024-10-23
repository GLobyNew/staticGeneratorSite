from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    allowed_text_types = (TextType.BOLD, TextType.ITALIC,
                          TextType.CODE, TextType.TEXT)
    if text_type not in allowed_text_types:
        raise Exception(
            "Can't split nodes: split_nodes_delimiter accepts only Bold, Italic, Code or Text")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
        else:
            splitted_node_text = node.text.split(delimiter)
            if len(splitted_node_text) % 2 == 0:
                raise ValueError("Invalid Markdown: delimiter not closed")
            for i in range(len(splitted_node_text)):
                if splitted_node_text[i] != "":
                    if i % 2 != 0:
                        new_nodes.append(
                            TextNode(splitted_node_text[i], text_type))
                    else:
                        new_nodes.append(
                            TextNode(splitted_node_text[i], TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # Get images from the text
        extracted_images = extract_markdown_images(node.text)

        # If no images found, just add node
        if len(extracted_images) == 0:
            new_nodes.append(node)
            continue

        # Removing images from original text
        original_text = node.text
        for image in extracted_images:
            splitted_text = original_text.split(
                f"![{image[0]}]({image[1]})", 1)
            if len(splitted_text) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if splitted_text[0] != "":
                new_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = splitted_text[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # Get links from the text
        extracted_links = extract_markdown_links(node.text)

        # If no links found, just add node
        if len(extracted_links) == 0:
            new_nodes.append(node)
            continue

        # Removing links from original text
        original_text = node.text
        for link in extracted_links:
            splitted_text = original_text.split(
                f"[{link[0]}]({link[1]})", 1)
            if len(splitted_text) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if splitted_text[0] != "":
                new_nodes.append(TextNode(splitted_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = splitted_text[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    inital_node = [TextNode(text, TextType.TEXT)]
    converting_node = split_nodes_delimiter(inital_node, "`", TextType.CODE)
    converting_node = split_nodes_delimiter(
        converting_node, "**", TextType.BOLD)
    converting_node = split_nodes_delimiter(
        converting_node, "*", TextType.ITALIC)
    converting_node = split_nodes_image(converting_node)
    ready_nodes = split_nodes_link(converting_node)
    return ready_nodes

   

