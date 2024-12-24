class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
          self.tag = tag
          self.value = value
          self.children = children
          self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def __eq__(Node1, Node2):
        if Node1.tag == Node2.tag:
            if Node1.value == Node2.value:
                if Node1.children == Node2.children:
                    if Node1.props == Node2.props:
                        return True
        return False

    def props_to_html(self):
        string_to_print = ""
        if self.props == None:
            return string_to_print
        for prop in self.props:
            string_to_print += f' {prop}="{self.props[prop]}"'
        return string_to_print

    def __repr__(self):
        return f"Tag={self.tag} Value={self.value} Children={self.children} Props={self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
