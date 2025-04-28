from enum import Enum

class TextType(Enum):
    normal_text = ""
    bold_text = "**"
    italic_text = "_"
    code_text = "`"
    link = "[anchor text](url)"
    image = "![alt text](url)"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, textNode):
        if (self.text == textNode.text and
            self.text_type == textNode.text_type and
            self.url == textNode.url):
            return True
        return False
    
    def __repr__(self):
        return (f"TextNode({self.text}, {self.text_type.value}, {self.url})")