from lxml.etree import _Element

class Node:
    body_link_chars = 0 # Hyperlink characters count under body tag
    body_chars = 0 # Characters count under body tag

    def __init__(self, tag=""):
        self.td = 0    # Text density
        self.ctd = 0    # Composite text density
        self.children = []  # Children node
        self.el = None  # Actual element - http://lxml.de/api/lxml.etree._Element-class.html
        self.tag = ""   # Trimmed element tag
        self.chars = 0  # Characters count
        self.tags = 1   # Tags count
        self.all_chars = 0  # All characters count
        self.all_tags = 1   # All tags count
        self.link_chars = 0 # Hyperlink characters count
        self.non_link_chars = 0 # Non-hyperlink characters count
        self.link_tags = 0  # Hyperlink tags count
        self.is_content = False
        self.duplicate_count = 0
        self.parent_count = 0
        self.same_child_count = []
        self.largest_child_trait = {}

        self.prev_sibling = None
        self.next_sibling = None
        self.child_distance_matrix = None
        self.preorder_pos = 0
        self.relative_pos = 0
        self.data_regions = None
        self.aligned = None

        if tag != "":
            self.el = _Element()
            self.el.tag = tag        
    
    def is_same(e1, e2):    # Compare if two elements are the same instance
        if e1 == None or e2 == None:
            return False
        if e1.tag != e2.tag:
            return False
        if e1.text != e2.text:
            return False
        if e1.tail != e2.tail:
            return False
        if e1.attrib != e2.attrib:
            return False
        if len(e1) != len(e2):
            return False

        return all(Node.is_same(c1, c2) for c1, c2 in zip(e1, e2))

    def height(self):
        if len(self.children) == 0:
            return 1
        else:
            child_heights = []

            for child in self.children:
                child_heights.append(child.height())

            return max(child_heights) + 1

    def to_preorder_string(self):
        sw = []

        sw.append(str(self.el.tag))

        for child in self.children:
            sw.extend(child.to_preorder_string())

        return sw
    
    def get_child_at_preorder_position(self, preorder_pos):
        if self.preorder_pos == preorder_pos:
            return self
        else:
            for child in self.children:
                sub_node = child.get_child_at_preorder_position(preorder_pos)

                if sub_node != None:
                    return sub_node
                else:
                    continue

            return None
