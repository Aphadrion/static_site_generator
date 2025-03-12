import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            nodes_list.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.NORMAL))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        nodes_list.extend(split_nodes)
        # Inside split_nodes_delimiter
    
    
    return nodes_list           

def extract_markdown_images(text):
    tuples = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return tuples

def extract_markdown_links(text):
    tuples = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return tuples

def split_nodes_image(old_nodes):
    nodes_list = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            nodes_list.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            nodes_list.append(node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                nodes_list.append(TextNode(sections[0], TextType.NORMAL))
            nodes_list.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            nodes_list.append(TextNode(original_text, TextType.NORMAL))
    return nodes_list

def split_nodes_link(old_nodes):
    nodes_list = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            nodes_list.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            nodes_list.append(node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                nodes_list.append(TextNode(sections[0], TextType.NORMAL))
            nodes_list.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            nodes_list.append(TextNode(original_text, TextType.NORMAL))
    return nodes_list

def text_to_textnodes(text):
    node = TextNode(text, TextType.NORMAL)
    nodes_list = split_nodes_delimiter([node], "`", TextType.CODE)
    nodes_list = split_nodes_delimiter(nodes_list, "**", TextType.BOLD)
    nodes_list = split_nodes_delimiter(nodes_list, "_", TextType.ITALIC)

    nodes_list = split_nodes_image(nodes_list)
    nodes_list = split_nodes_link(nodes_list)
    return nodes_list

'''
if __name__ == "__main__":
    text = "_italic_ and **bold** and `code` and ![alt text](/image.png) and [a link](/link)"
    initial_node = TextNode(text, TextType.NORMAL)
    nodes_list = text_to_textnodes(initial_node.text)
    for node in nodes_list:
        print(f"Text: {node.text}, Type: {node.text_type}, Extra: {node.url}")
'''
