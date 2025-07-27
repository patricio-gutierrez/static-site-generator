from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have tag")
        if not self.children:
            raise ValueError("All parent nodes must have children")
        html_tag = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_tag += child.to_html()
        html_tag += f"</{self.tag}>"
        return html_tag

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
