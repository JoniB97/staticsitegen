from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)  # Skip non-TEXT nodes, as these are already formatted
            continue

        sections = node.text.split(delimiter)  # Get sections by splitting
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")  # if equal = uneven formatters
        
        split_nodes = []
        for i in range(len(sections)):
            if sections[i] == "":
                continue  # Skip empty segments
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT)) # Return as TextType TEXT if outside markdown formatters
            else:
                split_nodes.append(TextNode(sections[i], text_type)) # Return as text_type if inside markdown formatters

        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        delimiters = extract_markdown_images(node.text)
        working_text = node.text
        for image_alt, image_url in delimiters:
            sections = working_text.split(f"![{image_alt}]({image_url})", 1)
            if len(sections[0]) > 0:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            working_text = sections[1]
        if len(working_text) > 0:
            new_nodes.append(TextNode(working_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        delimiters = extract_markdown_links(node.text)
        working_text = node.text
        for link_text, link_url in delimiters:
            sections = working_text.split(f"[{link_text}]({link_url})", 1)
            if len(sections[0]) > 0:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            working_text = sections[1]
        if len(working_text) > 0:
            new_nodes.append(TextNode(working_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = []
    starting_node = [TextNode(text, TextType.TEXT)]
    bold_nodes= split_nodes_delimiter(starting_node, "**", TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
    image_nodes = split_nodes_link(code_nodes)
    link_nodes = split_nodes_image(image_nodes)
    nodes = link_nodes

    return nodes

def main():
    test_image = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    test_link = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_images(test_image))
    print(extract_markdown_images(test_link))
    print(extract_markdown_links(test_image))
    print(extract_markdown_links(test_link))

if __name__ == "__main__":
    main()