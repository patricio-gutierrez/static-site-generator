from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None, alt = None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url
        self.alt = alt

    def __eq__(self, other):
        return self.text == other.text and self.text_type.value == other.text_type.value and self.url == other.url and self.alt == other.alt

    def __repr__(self):
        result = f"TextNode({self.text}, {self.text_type.value}"
        if self.url is not None:
            result += f", {self.url}"
        if self.alt is not None:
            result += f", {self.alt}"
        result += ")"
        return result
