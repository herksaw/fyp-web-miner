class Node:
    body_link_chars = 0 # Hyperlink characters count under body tag
    body_chars = 0 # Characters count under body tag

    def __init__(self):
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
    
