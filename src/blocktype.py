from enum import Enum
from htmlnode import *
from htmlnode import LeafNode, ParentNode
from textnode import text_node_to_html_node
from functions import text_to_textnodes
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split("\n\n") if block.strip()]
    return blocks

def block_to_block_type(markdown):
    lines = markdown.splitlines()

    if not lines:
        return BlockType.PARAGRAPH

    if lines[0].startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif lines[0].strip() == "```" and lines[-1].strip() == "```":
        return BlockType.CODE
    elif all(line.strip().startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    # Split the full markdown text into separate blocks
    blocks = markdown_to_blocks(markdown)
    html_children = []

    for block in blocks:
        # Determine the block type (heading, list, paragraph, etc.)
        block_type = block_to_block_type(block)

        # Based on the type, handle the block and convert to corresponding HTML node
        if block_type == BlockType.HEADING:
            html_children.append(handle_heading_block(block))
        elif block_type == BlockType.CODE:
            html_children.append(handle_code_block(block))
        elif block_type == BlockType.QUOTE:
            html_children.append(handle_quote_block(block))
        elif block_type == BlockType.UNORDERED_LIST:
            html_children.append(handle_unordered_list_block(block))
        elif block_type == BlockType.ORDERED_LIST:
            html_children.append(handle_ordered_list_block(block))
        else:  # Default fallback: treat as paragraph
            html_children.append(handle_paragraph_block(block))

    # Wrap all HTML children in a single <div> parent node
    return ParentNode("div", html_children)

# Converts inline markdown text to a list of HTMLNodes
def text_to_children(text):
    # Step 1: convert markdown string to list of TextNodes
    # Step 2: convert each TextNode to corresponding HTMLNode
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

# Handles heading blocks like "# Title"
def handle_heading_block(block):
    # Count number of leading "#" to determine heading level
    level = block.count("#", 0, block.find(" "))
    text = block[level + 1:].strip()
    return ParentNode(f"h{level}", text_to_children(text))

# Handles code blocks surrounded by triple backticks
def handle_code_block(block):
    # Remove the ``` lines, and preserve internal content
    lines = block.strip().split("\n")
    code_lines = [line.strip() for line in lines[1:-1]]  # skip opening/closing ```
    code_content = "\n".join(code_lines) + "\n" # Remove leading/trailing newlines and spaces
    return ParentNode("pre", [LeafNode("code", code_content)])

# Handles quote blocks starting with ">"
def handle_quote_block(block):
    lines = [line.lstrip("> ").strip() for line in block.splitlines()]
    text = " ".join(lines)
    return ParentNode("blockquote", text_to_children(text))

# Handles unordered lists with lines starting in "- "
def handle_unordered_list_block(block):
    lines = block.splitlines()
    items = []
    for line in lines:
        text = line[2:].strip()  # Remove "- " prefix
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)

# Handles ordered lists with numbered prefixes like "1. Item"
def handle_ordered_list_block(block):
    lines = block.splitlines()
    items = []
    for line in lines:
        index = line.find(". ")
        if index != -1:
            text = line[index + 2:].strip()
            items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)

# Handles paragraphs (default block type)
def handle_paragraph_block(block):
    clean_text = " ".join(block.strip().splitlines())  # Join lines with a space
    clean_text = re.sub(r"\s+", " ", clean_text)       # Collapse multiple spaces to one
    return ParentNode("p", text_to_children(clean_text))
