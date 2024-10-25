from enum import Enum
from htmlnode import HTMLNode

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


def markdown_to_html_node(markdown):
    splitted_markdown = markdown_to_blocks(markdown)
    for block in splitted_markdown:
        block_type = block_to_block_type(block)
        match block_type:
            case "paragraph":
                new_node = HTMLNode()