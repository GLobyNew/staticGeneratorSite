from textnode import TextNode, TextType


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
