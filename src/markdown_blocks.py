from enum import Enum
from htmlnode import ParentNode, LeafNode
from splitters_n_extractors import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"


def markdown_to_blocks(markdown):
    list_of_str = markdown.splitlines()
    rdy_list = []
    combined_str = ""
    for value in list_of_str:
        if value != "":
            combined_str += value + '\n'
        else:
            rdy_list.append(combined_str)
            combined_str = ""
    if combined_str != "":
        rdy_list.append(combined_str)
    rdy_list = list(filter(lambda x: x != "", rdy_list))
    rdy_list = list(map(lambda x: x.strip(), rdy_list))
    return rdy_list


def block_to_block_type(markdown_block):
    if not len(markdown_block):
        raise ValueError("Markdown block has no text")
    # Check if it is a heading
    splitted_str = markdown_block.split()
    heading_level = splitted_str[0].count("#")
    if heading_level > 0 and heading_level < 7:
        return BlockType.HEADING
    if heading_level >= 7:
        raise Exception("Bad Markdown: Heading level has more than 7 levels")

    # Check if it's a code block
    if splitted_str[0] == "```" and splitted_str[-1] == "```":
        return BlockType.CODE
    # Handle code block if only one word
    if splitted_str[0][:3] == "```" and splitted_str[-1][-3:] == "```":
        return BlockType.CODE

    # Check if its quote block
    splitted_by_lines = markdown_block.splitlines()
    if all(x.startswith(">") for x in splitted_by_lines):
        return BlockType.QUOTE

    # Check if its unordered list block
    if all(x.startswith("* ") or x.startswith("- ") for x in splitted_by_lines):
        return BlockType.UNORDERED_LIST

    # Check if its ordered list block
    is_it_ordered = True
    i = 1
    for line in splitted_by_lines:
        if not line.startswith(f"{i}. "):
            is_it_ordered = False
            break
        i += 1
    if is_it_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def count_heading_level(heading_str):
    return heading_str.count("#")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = list(map(lambda x: x.text_node_to_html_node(), text_nodes))
    return html_nodes


def remove_heading_from_block(heading_block, heading_level):
    return heading_block[heading_level+1:]


def remove_code_from_block(code_block):
    return code_block[3:-3]


def remove_quote_from_block(quote_block):
    splitted_block = quote_block.splitlines()
    cleared_block = ""
    for line in splitted_block:
        cleared_block += line[1:] + "\n"
    return cleared_block

def remove_ordered_list_and_generate_children(list_blocks):
    splitted_block = list_blocks.splitlines()
    new_nodes = []
    for node in splitted_block:
        children = text_to_children(node[3:])
        new_nodes.append(ParentNode("li", children))
    return new_nodes


def remove_unordered_list_and_generate_children(list_blocks):
    splitted_block = list_blocks.splitlines()
    new_nodes = []
    for node in splitted_block:
        children = text_to_children(node[2:])
        new_nodes.append(ParentNode("li", children))
    return new_nodes


def markdown_to_html_node(markdown):
    splitted_markdown = markdown_to_blocks(markdown)
    new_nodes = []
    for block in splitted_markdown:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                children = text_to_children(block)
                new_node = ParentNode("p", children)
            case BlockType.HEADING:
                heading_level = count_heading_level(block)
                block = remove_heading_from_block(block, heading_level)
                children = text_to_children(block)
                new_node = ParentNode(f"h{heading_level}", children)
            case BlockType.CODE:
                block = remove_code_from_block(block)
                children = text_to_children(block)
                new_node = [ParentNode("code", children)]
                new_node = ParentNode("pre", new_node)
            case BlockType.QUOTE:
                block = remove_quote_from_block(block)
                children = text_to_children(block)
                new_node = ParentNode("blockquote", children)
            case BlockType.ORDERED_LIST:
                children = remove_ordered_list_and_generate_children(block)
                new_node = ParentNode("ol", children)
            case BlockType.UNORDERED_LIST:
                children = remove_unordered_list_and_generate_children(block)
                new_node = ParentNode("ul", children)
        new_nodes.append(new_node)
    return ParentNode("div", new_nodes)



