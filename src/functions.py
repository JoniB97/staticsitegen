from textnode import TextType, TextNode

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