from enum import Enum
from htmlnode import *
from textnode import *
from inlinemarkdown import *
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []

    for block in blocks:
        if block != "":
            lines = [line.strip() for line in block.split("\n") if line.strip()]

            if block.lstrip().startswith("-") or block.lstrip().startswith("1."):
                clean_blocks.append("\n".join(lines))
            else:
                clean_blocks.append("\n".join(lines))
    return clean_blocks
    

def block_to_block_type(block):
    lines = [line.lstrip() for line in block.split("\n") if line.strip()]
    line = lines[0]

    if line.startswith("```") and lines[-1].startswith("```"):
        print("Detected Type: CODE")  # Debug
        return BlockType.CODE

    if line.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        print("Detected Type: HEADING")  # Debug
        return BlockType.HEADING
    
    if line.startswith(">"):
        for l in lines:
            if not l.startswith(">"):
                return BlockType.PARAGRAPH
        print("Detected Type: QUOTE")  # Debug
        return BlockType.QUOTE
    
    if line.startswith("- "):
        for l in lines:
            if not l.startswith("- "):
                return BlockType.PARAGRAPH
        print("Detected Type: UNORDERED_LIST")  # Debug
        return BlockType.UNORDERED_LIST
    
    num = 1
    if line.startswith(f"{num}. "):
        for l in lines:
            if not l.startswith(f"{num}. "):
                return BlockType.PARAGRAPH
            num += 1
        print("Detected Type: ORDERED_LIST")  # Debug
        return BlockType.ORDERED_LIST
        
    return BlockType.PARAGRAPH


#HTMLNode({self.tag}, {self.value}, {self.children}, {self.props}
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node = HTMLNode("div", None, [])

    for block in blocks:
        type = block_to_block_type(block)

        match type:
            case BlockType.PARAGRAPH:
                block_content = block.replace("\n", " ")
                parent_node.children.append(HTMLNode("p", None, text_to_children(block_content)))

            case BlockType.HEADING:
                level = 0
                for char in block:
                    if char == '#':
                        level += 1
                block = block[level:].strip()
                parent_node.children.append(HTMLNode(f"h{level}", None, text_to_children(block)))

            case BlockType.CODE:
                code_lines = block.split("\n")
                inner_lines = code_lines[1:-1]
                code_content = "\n".join(inner_lines) + "\n"
                text_node = TextNode(code_content, TextType.NORMAL)
                code_node = text_node_to_html_node(text_node)

                if code_node.tag != "code":
                    code_node = HTMLNode("code", None, [code_node])
                pre_node = HTMLNode("pre", None, [code_node])
                parent_node.children.append(pre_node)

            case BlockType.QUOTE:
                parent_node.children.append(HTMLNode("blockquote", None, text_to_children(block.lstrip('> ').strip())))

            case BlockType.UNORDERED_LIST:
                list = HTMLNode("ul", None, [])
                items = block.split("\n")
                for item in items:
                    if item.startswith("- "):
                        item_text = item[2:].strip()
                    elif item.startswith("* "):
                        item_text = item[2:].strip()
                    else:
                        item_text = item.strip()
                    
                    if item_text:
                        list.children.append(HTMLNode("li", None, text_to_children(item_text)))
                parent_node.children.append(list)

            case BlockType.ORDERED_LIST:
                list = HTMLNode("ol", None, [])
                items = block.split("\n")
                for item in items:
                    parts = item.split(". ", 1)
                    if len(parts) > 1:
                        item_text = parts[1].strip()
                    else:
                        item_text = item.strip()
                    if item_text:
                        list.children.append(HTMLNode("li", None, text_to_children(item_text)))
                parent_node.children.append(list)

            case _:
                raise Exception("invalid BlockType")
    return parent_node

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")