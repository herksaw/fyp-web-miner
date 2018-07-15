class GeneralizedNode:
    SELF = 0
    CHILD_CONT = 1
    CHILD_NON_CONT = 2

    def __init__(self):
        self.nodes = []
        self.data_record_indicator = -1

    def add(self, node):
        self.nodes.append(node)

    def get_nodes(self):
        return self.nodes

    def get(self, i):
        return self.nodes[i]

    def size(self):
        return len(self.nodes)
        