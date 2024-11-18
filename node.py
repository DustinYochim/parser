
class Node:
    """
    This class represents a Node which consist of a label, left node, right node, and a list consisting
    of tokens.
    """
    def __init__(self, label):
        self.label = label
        self.tokens = []
        self.children = []

    def add_child(self, child):
        # if child:
            self.children.append(child)

    def add_token(self, token):
        # if token:
            self.tokens.append(token)

    def print_self(self):
        """
        Print this node, used for testing.
        """
        print("Node(label = " + self.label + ", tokens = " + str(self.tokens))