
class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children # A list of HTMLNode objects representing the children of this node
        self.props = props # A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())

    
    def __repr__(self):
        children_repr = [repr(child) for child in self.children] if self.children else None
        return (f'HTMLNode(tag="{self.tag}", value="{self.value}", '
                f'children={children_repr}, props="{self.props_to_html()}")')
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )



# def main():
#     testNode = HTMLNode("Tag", "Value", [], {"href": "https://www.google.com", "target": "_blank"})
#     # string = testNode.props_to_html()
#     print(testNode)

# main()