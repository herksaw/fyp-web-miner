# import operator
from functools import total_ordering

@total_ordering
class Tree:
    PRE_ORDER = 0
    POST_ORDER = 1

    def __init__(self, root):
        self.root = root

    def get_root(self):
        return self.root

    def size(self):
        return len(self.traverse(Tree.PRE_ORDER))

    def traverse(self, traverse_type):
        traverse_list = []

        if traverse_type == Tree.PRE_ORDER:
            pre_order(self.get_root(), traverse_list)
        elif traverse_type == Tree.POST_ORDER:
            post_order(self.get_root(), traverse_list)
        else:
            traverse_list = None

        return traverse_list

    def pre_order(self, node, traverse_list):
        traverse_list.append(node)

        for child in node.children:
            self.pre_order(child, traverse_list)

    def post_order(self, node, traverse_list):
        traverse_list.append(node)

        children = node.children

        for i in range(len(children) - 1, -1, -1):
            self.post_order(children[i], traverse_list)

    def __lt__(self, other):
        return self.size() > other.size()

    def __gt__(self, other):
        return self.size() < other.size()

    def __eq__(self, other):
        return self.size() == self.size()

    def simple_tree_matching(self, b):
        if self.get_root().el.tag != b.get_root().el.tag:
            b.get_root().aligned = True

            return 0
        else:
            m = len(self.get_root().children)
            n = len(b.get_root().children)

            matrix = [[None for x in range(n + 1)] for y in range(m + 1)]

            for i in range(0, m + 1, 1):
                matrix[i][0] = 0

            for j in range(0, n + 1, 1):
                matrix[0][j] = 0

            for i in range(1, m + 1, 1):
                for j in range(1, n + 1, 1):
                    ai = Tree(self.get_root().children[i - 1])
                    bj = Tree(b.get_root().children[j - 1])

                    wij = ai.simple_tree_matching(bj)

                    matrix[i][j] = max(max(matrix[i][j - 1], matrix[i - 1][j]), matrix[i - 1][j - 1] + wij)

            return matrix[m][n] + 1

    def get_subtree_by_preorder(self, preorder_pos):
        subtree_root = self.get_root().get_child_at_preorder_position(preorder_pos)

        return Tree(subtree_root)
