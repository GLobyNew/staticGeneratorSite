class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html = " "
        if self.props is not None:
            for prop in self.props:
                html += f"{prop}=\"{self.props.get(prop)}\" "
        return html[:-1]

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        html_string = ""
        if self.tag is None:
            raise ValueError("ParentNode doesn't have any tag")
        if self.children is None:
            raise ValueError("Children is required")
        # if len(self.children) == 0:
        #     return f"<{self.tag}>{self.value}</{self.tag}>"
        for node in self.children:
            html_string += node.to_html()
        return f"<{self.tag}>{html_string}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode doesn't have any value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props}"
